from collections import defaultdict

from Bio import pairwise2
from Bio.pairwise2 import format_alignment
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
    if not value_list:
        return None
    return max(set(value_list), key = value_list.count)

def sort_by_time(utterances):
        return sorted(utterances, key=lambda x: x['start'])

def concat_adjacent_speaker_utterances(utterances):
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

def align_texts(text1, text2, char_level=False):
    text1 = utils.normalize_text(text1, char_level=char_level)
    #print(text1)
    text2 = utils.normalize_text(text2, char_level=char_level)
    #print(text2)
    if not text1 or not text2:
        return 0, max(len(text1), len(text2)), None
    alignments = pairwise2.align.globalxs(text1, text2, one_alignment_only=True, gap_char=['-'], open=-1, extend=-1)
    #print(alignments[0][0])
    #print(alignments[0][1])
    #print(format_alignment(*alignments[0]))

    agree, disagree = 0, 0
    for a, b in zip(alignments[0][0], alignments[0][1]):
        if a == b:
            agree += 1
        else:
            disagree += 1
    return agree, disagree, alignments[0]

                     
class BioAligner:
    def __init__(self):
        pass
    
    def time_overlap(self, a, b) -> float:
        """
        Return the overlap of two time intervals
        if the intervals do not overlap, return the distance between them (always negative)
        """
        start1, end1 = a['start'], a['end']
        start2, end2 = b['start'], b['end']
        overlap = min(end1, end2) - max(start1, start2)
        return overlap

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
                candidates.append(i)
                if alignment[0][i]['end'] - alignment[1][idx]['start'] < -5:
                    break

        for i in range(idx + 1, len(alignment[0])):
            if alignment[0][i] != None:
                candidates.append(i)
                if  alignment[0][i]['start'] - alignment[1][idx]['end'] > 5:
                    break

        match_fn = lambda a, b: self.match_fn_with_threshold(a, b, threshold=0.5) # be less strict
        scores = [match_fn(alignment[0][c], alignment[1][idx]) for c in candidates]

        if len(scores) == 0 or max(scores) <= 0:
            return None
        return candidates[scores.index(max(scores))]

    def align_utterances(self, manual_utterances, other_utterances, both_manual=False):
        manual_utterances = sort_by_time(manual_utterances)
        concat_manual_utterances = concat_adjacent_speaker_utterances(manual_utterances)

        if not len(other_utterances):
            return [(tuple(u['original_utterances']), tuple()) for u in concat_manual_utterances]

        other_utterances = sort_by_time(other_utterances)
        concat_other_utterances = other_utterances
        if both_manual:
            concat_other_utterances = concat_adjacent_speaker_utterances(other_utterances)
        else:
            for idx, u in enumerate(other_utterances):
                other_utterances[idx]['original_utterances'] = [idx]

        match_fn = lambda a, b: self.match_fn_with_threshold(a, b, threshold=0.0) # be more strict
        alignment = pairwise2.align.globalcx(concat_manual_utterances, concat_other_utterances, one_alignment_only=True, gap_char=[None], match_fn=match_fn)

        alignments = []
        found_for_auto = set()
        # collect alignments
        # if there is no auto utterance, we need to find the best alignment matching the manual utterance
        for idx, (manual_utt, auto_utt) in enumerate(zip(alignment[0][0], alignment[0][1])):
            if auto_utt is None:
                continue
            if manual_utt is None:
                manual_utt_idx = self.find_best_alignment_for_auto(alignment[0], idx)
                if manual_utt_idx is not None:
                    manual_utt = alignment[0][0][manual_utt_idx]
                    found_for_auto.add(manual_utt_idx)
            alignments.append((tuple(manual_utt['original_utterances'] if manual_utt else []), tuple(auto_utt['original_utterances'])))
        # add auto utterances for which we did not find a manual utterance as missing alignments
        for idx, (manual_utt, auto_utt) in enumerate(zip(alignment[0][0], alignment[0][1])):
            if auto_utt is not None:
                continue
            if idx in found_for_auto:
                continue
            alignments.append((tuple(manual_utt['original_utterances']), tuple([])))

        return list(group_alignments(alignments))

class MatrixAligner:

    def __init__(self, threshold_overlap=0.5):
        self.threshold_overlap = threshold_overlap
        self.lexical_similarity_f = NormalizedLevenshtein().similarity

    def get_utterance_similarity(self, utt1, utt2):
        time_overlap = self.get_time_overlap(utt1, utt2)
        if time_overlap == 0:
            return 0
        lex_similarity = self.lexical_similarity_f(utt1['text'], utt2['text'])
        return (lex_similarity + time_overlap) / 2

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

    def align_utterances(self, manual_utterances, other_utterances, both_manual=False):
        manual_utterances = sort_by_time(manual_utterances)
        concat_manual_utterances = concat_adjacent_speaker_utterances(manual_utterances)

        other_utterances = sort_by_time(other_utterances)
        concat_other_utterances = other_utterances
        if both_manual:
            concat_other_utterances = concat_adjacent_speaker_utterances(other_utterances)
        else:
            for idx, u in enumerate(other_utterances):
                other_utterances[idx]['original_utterances'] = [idx]

        overlap_matrix = np.zeros((len(concat_manual_utterances), len(concat_other_utterances)))
        for i, u1 in enumerate(concat_manual_utterances):
            for j, u2 in enumerate(concat_other_utterances):
                overlap_matrix[i, j] = self.get_utterance_similarity(u1, u2)

        #print_overlap_matrix(overlap_matrix)

        # this is here just for debugging reasons
        # it prints out the utterances that have more than 2 overlapping utterances
        # nonzeros = np.nonzero(overlap_matrix)
        # nonzero_count_cols = np.count_nonzero(overlap_matrix, axis=0)
        # print("nonzero_count_cols", nonzero_count_cols)
        # for j in range(len(nonzero_count_cols)):
        #     if nonzero_count_cols[j] > 2:
        #         print(">2 AUTO: " + other_utterances[j]['text'])
        #         i_list = [i for i, j2 in zip(nonzeros[0], nonzeros[1]) if j2 == j]
        #         for i in i_list:
        #             print(f">2 MANUAL: [{overlap_matrix[i, j]}] " + " ".join([manual_utterances[k]['text'] for k in concat_manual_utterances[i]['original_utterances']]))
        #         print()

        alignments = self._find_alignment_in_matrix(overlap_matrix)
        #self.print_overlap_matrix(alignmnents_to_matrix(alignments))

        aligned_manual, aligned_other = set(), set()
        for manual_idx, other_idx in alignments:
            aligned_manual.add(manual_idx)
            aligned_other.add(other_idx)
        for manual_idx in range(len(concat_manual_utterances)):
            if manual_idx not in aligned_manual:
                alignments.append((manual_idx, None))
        for other_idx in range(len(concat_other_utterances)):
            if other_idx not in aligned_other:
                alignments.append((None, other_idx))

        alignments_in_orig = []
        for manual_idx, other_idx in alignments:
            manual_utt, other_utt = [], []
            if manual_idx is not None:
                manual_utt = concat_manual_utterances[manual_idx]['original_utterances']
            if other_idx is not None:
                other_utt = concat_other_utterances[other_idx]['original_utterances']
            alignments_in_orig.append((manual_utt, other_utt))

        return list(group_alignments(alignments_in_orig))


# OBSOLETE CODE

def concat_texts_by_speaker(utterances):
    speakers = set([u['speaker'] for u in utterances])
    texts = {}
    for speaker in speakers:
        texts[speaker] = ' '.join([u['text'] for u in utterances if u['speaker'] == speaker])
    return speakers, texts