from collections import defaultdict

from Bio import pairwise2
import networkx as nx
import numpy as np
from scipy.optimize import linear_sum_assignment
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

import utils

def print_overlap_matrix(overlap_matrix):
    for i in range(overlap_matrix.shape[0]):
        print(i, end=' ')
        for j in range(overlap_matrix.shape[1]):
            print(f"{overlap_matrix[i, j]:.1f}" if overlap_matrix[i, j] else f"   ", end=' ')
        print()

def extract_text(l, annotation):
    return " ".join([annotation[i]['text'] for i in l])

def extract_speaker(l, annotation):
    value_list = [annotation[i]['speaker'] for i in l]
    return max(set(value_list), key = value_list.count)

def group_alignments(alignments):
    G = nx.Graph()
    for a, b in alignments:
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        for i in a:
            G.add_node(f"a_{i}")
        for j in b:
            G.add_node(f"b_{j}")
        for i in a:
            for j in b:
                G.add_edge(f"a_{i}", f"b_{j}")
    for component in nx.connected_components(G):
        a = [int(node[2:]) for node in component if node.startswith('a')]
        b = [int(node[2:]) for node in component if node.startswith('b')]
        yield (tuple(sorted(a)), tuple(sorted(b)))
    
                     
class BioAligner:
    def __init__(self):
        pass

    def sort_by_time(self, utterances):
        return sorted(utterances, key=lambda x: x['start'])

    def concat_adjacent_speaker_utterances(self, utterances):
        if len(utterances) == 0:
            return []
        new_utterances = [utterances[0].copy()]
        new_utterances[-1]['original_utterances'] = [0]

        for idx, u in enumerate(utterances[1:]):
            if new_utterances[-1]['speaker'] == u['speaker']:
                new_utterances[-1]['text'] += ' ' + u['text']
                new_utterances[-1]['end'] = u['end']
                new_utterances[-1]['original_utterances'].append(idx + 1)
            else:
                new_utterances.append(u.copy())
                new_utterances[-1]['original_utterances'] = [idx + 1]
        return new_utterances
    
    def time_overlap(self, a, b) -> float:
        """
        Return the overlap of two time intervals
        if the intervals do not overlap, return the distance between them
        """
        if a['start'] > b['end'] or b['start'] > a['end']:
            return min(a['end'], b['end']) - max(a['start'], b['start'])
        return min(a['end'], b['end']) - max(a['start'], b['start'])

    def text_score(self, a, b):
        a, b = utils.normalize_text(a['text'], char_level=True), utils.normalize_text(b['text'], char_level=True)
        if len(a) == 0 or len(b) == 0:
            return 0
        alignment = pairwise2.align.globalms(a, b, one_alignment_only=True, gap_char=['-'], open=0, extend=0, match=1, mismatch=0)
        return alignment[0].score

    def match_fn_with_threshold(self, a, b, threshold=0.1):
        overlap = self.time_overlap(a, b)
        if overlap < -threshold:
            return float('-inf')
        l = b['end'] - b['start']
        return (overlap / l) * self.text_score(a, b) / max(1, len(utils.normalize_text(b['text'], char_level=True)))
    
    def find_best_alignment_for_auto(self, alignment, idx):
        candidates = []
        for i in range(idx - 1, -1, -1):
            if alignment[0][i] != None:
                candidates.append(alignment[0][i])
            '''
            we need at least 2 utterances
            since the manual transcript is concatenated
            we know the 2 utterances have different speakers
            '''
            if len(candidates) > 1:  
                break

        for i in range(idx + 1, len(alignment[0])):
            if alignment[0][i] != None:
                candidates.append(alignment[0][i])
            if len(candidates) > 3: # two utterances from the right side
                break

        match_fn = lambda a, b: self.match_fn_with_threshold(a, b, threshold=0.5) # be less strict
        scores = [match_fn(c, alignment[1][idx]) for c in candidates]

        if len(scores) == 0 or max(scores) <= 0:
            return None
        return candidates[scores.index(max(scores))]

    def align_utterances(self, manual_utterances, other_utterances):
        manual_utterances = self.sort_by_time(manual_utterances)
        manual_utterances = self.concat_adjacent_speaker_utterances(manual_utterances)

        other_utterances = self.sort_by_time(other_utterances)
        for idx, u in enumerate(other_utterances):
            other_utterances[idx]['original_utterances'] = [idx]

        match_fn = lambda a, b: self.match_fn_with_threshold(a, b, threshold=0.0) # be more strict
        alignment = pairwise2.align.globalcx(manual_utterances, other_utterances, one_alignment_only=True, gap_char=[None], match_fn=match_fn)

        alignments = []
        for idx, (a, b) in enumerate(zip(alignment[0][0], alignment[0][1])):
            if b is not None:
                al = []
                if a is None:
                    a = self.find_best_alignment_for_auto(alignment[0], idx)
                if a is not None:
                    al.extend(a['original_utterances'])
                alignments.append((tuple(al), tuple(b['original_utterances'])))

        return group_alignments(alignments)

class MatrixAligner:

    def __init__(self, threshold_overlap=0.5):
        self.threshold_overlap = threshold_overlap
        self.lexical_similarity_f = NormalizedLevenshtein().similarity

    def get_utterance_similarity(self, utt1, utt2):
        time_overlap = self.get_time_overlap(utt1, utt2)
        if time_overlap == 0:
            return 0
        lex_similarity = self.lexical_similarity_f(utt1['text'], utt2['text'])
        return lex_similarity * time_overlap

    def get_time_overlap(self, utt1, utt2):
        start1, end1 = utt1['start'], utt1['end']
        start2, end2 = utt2['start'], utt2['end']
        overlap = max(0, min(end1, end2) - max(start1, start2) - self.threshold_overlap)
        return overlap

    def _find_alignment_in_matrix(self, m):
        nonzeros = np.nonzero(m)
        nonzero_count_cols = np.count_nonzero(m, axis=0)
        nonzero_count_rows = np.count_nonzero(m, axis=1)
        singletons = []
        for i, j in zip(nonzeros[0], nonzeros[1]):
            singleton_row, singleton_col = False, False
            if nonzero_count_cols[j] == 1:
                singleton_col = True
            if nonzero_count_rows[i] == 1:
                singleton_row = True
            if singleton_col or singleton_row:
                singletons.append((i, j, singleton_row, singleton_col))
        #print(singletons)
        alignment = []
        for idx, singleton_tuple in enumerate(singletons):
            i, j, is_row, is_col = singleton_tuple
            if idx > 0:
                prev_i, prev_j, prev_is_row, prev_is_col = singletons[idx - 1]
                if prev_is_col:
                    prev_j += 1
                if prev_is_row:
                    prev_i += 1
                new_i, new_j = i, j
                if is_col:
                    new_j -= 1
                if is_row:
                    new_i -= 1
                submatrix = m[prev_i:new_i+1, prev_j:new_j+1]
                if submatrix.size > 1:
                    #print(f"m[{prev_i}:{new_i}+1, {prev_j}:{new_j}+1] = {submatrix}")
                    submatrix_rows, submatrix_cols = linear_sum_assignment(submatrix, maximize=True)
                    for submatrix_row, submatrix_col in zip(submatrix_rows, submatrix_cols):
                        if submatrix[submatrix_row, submatrix_col] == 0:
                            continue
                        #print(f"{prev_i = } {submatrix_row = } {prev_j = } {submatrix_col = }")
                        alignment.append(((prev_i + submatrix_row).item(), (prev_j + submatrix_col).item()))
            #print(f"{i = }, {j = }")
            alignment.append((i.item(), j.item()))
        return alignment

    def alignmnents_to_matrix(self, alignments):
        x_len = max([a[0] for a in alignments]) + 1
        y_len = max([a[1] for a in alignments]) + 1
        m = np.zeros((x_len, y_len))
        for i, j in alignments:
            m[i, j] = 1
        return m

    # def _group_alignment(self, alignment):
    #     ltr_alignment_dict = defaultdict(list)
    #     rtl_alignment_dict = defaultdict(list)
    #     for i, j in alignment:
    #         ltr_alignment_dict[i].append(j)
    #         rtl_alignment_dict[j].append(i)
    #     grouped_alignment = []
    #     for i, j_list in ltr_alignment_dict.items():
    #         i_list = [i]
    #         if len(j_list) == 1:
    #             i_list = rtl_alignment_dict[j_list[0]]
    #         align = (tuple(i_list), tuple(j_list))
    #         if align not in grouped_alignment:
    #             grouped_alignment.append(align)
    #     return grouped_alignment

    def align_utterances(self, annot1, annot2, grouped=True):
        overlap_matrix = np.zeros((len(annot1), len(annot2)))
        for i, u1 in enumerate(annot1):
            for j, u2 in enumerate(annot2):
                overlap_matrix[i, j] = self.get_utterance_similarity(u1, u2)

        print_overlap_matrix(overlap_matrix)
        alignments = self._find_alignment_in_matrix(overlap_matrix)
        #self.print_overlap_matrix(alignmnents_to_matrix(alignments))
        if not grouped:
            return alignments
        
        return group_alignments(alignments)