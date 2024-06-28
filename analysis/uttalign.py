from collections import defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

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

class UtteranceAligner:

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
                        alignment.append((prev_i + submatrix_row, prev_j + submatrix_col))
            #print(f"{i = }, {j = }")
            alignment.append((i, j))
        return alignment

    def alignmnents_to_matrix(self, alignments):
        x_len = max([a[0] for a in alignments]) + 1
        y_len = max([a[1] for a in alignments]) + 1
        m = np.zeros((x_len, y_len))
        for i, j in alignments:
            m[i, j] = 1
        return m

    def _group_alignment(self, alignment):
        ltr_alignment_dict = defaultdict(list)
        rtl_alignment_dict = defaultdict(list)
        for i, j in alignment:
            ltr_alignment_dict[i].append(j)
            rtl_alignment_dict[j].append(i)
        grouped_alignment = []
        for i, j_list in ltr_alignment_dict.items():
            i_list = [i]
            if len(j_list) == 1:
                i_list = rtl_alignment_dict[j_list[0]]
            align = (tuple(i_list), tuple(j_list))
            if align not in grouped_alignment:
                grouped_alignment.append(align)
        return grouped_alignment

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
        
        grouped_alignment = self._group_alignment(alignments)
        return grouped_alignment