"""Find timestamps to split the recording into individual exercises.

This script attempts to find timestamps that would split the recording into individual exercises.
It is carried out on the transcript of the recording by matching the words and phrases
that the examiner typically says to introduce or conclude an exercise.
"""

from collections import OrderedDict
import logging
import re
import sys
import xml.etree.ElementTree as ET

EXER_REGEX = r'([uúUÚ]lo[hz]|úlovu)'
NUMCARD_REGEXS = [r'([jJ]edna|1)', r'([dD]v[aě]|2)', r'([tT]ři|3)']
NUMORD_REGEXS = [r'[Pp]rv', r'[Dd]ruh', r'[Tt]řet']
EXER_END_REGEX_PARTS = [r'[Kk]onec', r'([uú]lo[zvh][ey]|důvěr)']

def matches_exer(text, exer_idx=0):
    # regexes to match any occurence of the exercise; the first one should be the start
    # "exercise I"
    EXER_I_REGEX = EXER_REGEX + r'.*' + NUMCARD_REGEXS[exer_idx]
    # "Ith exercise"
    ITH_EXER_REGEX = NUMORD_REGEXS[exer_idx] + r'.*' + EXER_REGEX
    return re.search(EXER_I_REGEX, text) or re.search(ITH_EXER_REGEX, text)

def matches_exer_end(text, exer_idx=0):
    # regexes to match end of the exercise
    # "end of exercise I"
    EXER_I_END_REGEX = EXER_END_REGEX_PARTS[0] + r'.*' + EXER_END_REGEX_PARTS[1] + r'.*' + NUMCARD_REGEXS[exer_idx]
    # "end of Ith exercise"
    ITH_EXER_END_REGEX = EXER_END_REGEX_PARTS[0] + r'.*' + NUMORD_REGEXS[exer_idx] + r'.*' + EXER_END_REGEX_PARTS[1]
    #logging.debug(f"{EXER_I_END_REGEX = }")
    #logging.debug(f"{ITH_EXER_END_REGEX = }")
    return re.search(EXER_I_END_REGEX, text) or re.search(ITH_EXER_END_REGEX, text)

def find_exercise_starts_ends(u_elems_sorted):
    exer_offset = None
    exer_starts = []
    exer_ends = []

    postponed_start = False
    
    for u_elem in u_elems_sorted:

        if exer_offset is None:
            for i in range(len(NUMCARD_REGEXS)):
                if matches_exer(u_elem.text, i):
                    exer_offset = i
                    break
            else:
                continue

        if postponed_start:
            postponed_start = False
            exer_starts.append(u_elem)

        is_end = False
        # search for the end of the exercise no. I, only if it has already started
        if len(exer_starts) > len(exer_ends) and matches_exer_end(u_elem.text, exer_offset + len(exer_ends)):
            is_end = True
            exer_ends.append(u_elem)

        # search for the start of the exercise no. I, unless it has already started
        if len(exer_starts) == len(exer_ends) and matches_exer(u_elem.text, exer_offset + len(exer_starts)):
            # the end of the previous exercise and the start of the new exercise appear in the same utterance
            # save the start time of the following utterance
            if is_end:
                postponed_start = True
                continue
            exer_starts.append(u_elem)
        
    return exer_starts, exer_ends

def interactive_debugging(exer_starts, exer_ends, total_start, total_end, filename=""):
    print(f"Start: {total_start}")
    for i in range(len(exer_ends)):
        print(f"({i+1})\t[{exer_starts[i].attrib['start']:10}]\t{exer_starts[i].text}")
        print(f"   \t[{exer_ends[i].attrib['end']:10}]\t{exer_ends[i].text}")
    if len(exer_starts) > len(exer_ends):
        i = len(exer_starts) - 1
        print(f"({i+1})\t[{exer_starts[i].attrib['start']:10}]\t{exer_starts[i].text}")
    print(f"End: {total_end}")
    
    answer = input("Is this OK (y/n) # comment? ")
    if not answer.lower().startswith("y"):
        _, comment = answer.split("#")
        print()
        print(f"[ERR]\t{filename}\t{comment}")

def main():
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    filename = sys.argv[1]
    doctree = ET.parse(filename)
    text_elem = doctree.find(".//text")
    # sorting utterances by their start times
    u_elems_sorted = sorted(text_elem.findall("./u"), key=lambda elem: float(elem.get("start")))

    exer_starts, exer_ends = find_exercise_starts_ends(u_elems_sorted)
    total_start = u_elems_sorted[0].attrib['start']
    total_end = u_elems_sorted[-1].attrib['end']

    interactive_debugging(exer_starts, exer_ends, total_start, total_end, filename=filename)

if __name__ == "__main__":
    main()
