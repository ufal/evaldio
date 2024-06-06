"""Normalization of the TEITOK annotated transcripts.

This scripts normalizes the annotated transcripts in the TEITOK format
coming from manual annotation.
The normalization includes:
    - sorting utterances by their start times
    - remove other attributes than "start", "end", and "who"
    - re-index IDs
    - standardization of speakers' names, guessing the examiner by the content: EXAM_1, CAND_1, CAND_2, ..., CAND_N
"""

from collections import OrderedDict
import logging
import re
import sys
import xml.etree.ElementTree as ET

def estimate_examiner_role(texts):
    pattern_counts = [
        sum([re.search(pattern, t) is not None for t in texts])
        for pattern in [
            r"[Úú]lo[hz]",
            r"[Oo]táz[ek]",
            r"[Bb]ud[ue]"
        ]
    ]
    return (sum(pattern_counts) / len(texts)) / len(pattern_counts)

def guess_speaker_roles(u_elems):
    utt_by_speakers = OrderedDict()
    for u_elem in u_elems:
        utt_by_speakers.setdefault(u_elem.attrib["who"], []).append(u_elem.text)
    old_speakers = list(utt_by_speakers.keys())
    # a singler speaker is supposed to be the candidate
    assert len(old_speakers) >= 1
    if len(old_speakers) == 1:
        return {old_speakers[0]: "CAND_1"}
    name_assign = {}
    # find the examiner
    examiner = max(old_speakers, key=lambda speaker: estimate_examiner_role(utt_by_speakers[speaker]))
    name_assign[examiner] = "EXAM_1"
    old_speakers.remove(examiner)
    # remaining speakers are candidates
    # their idx is assigned in the order they first appear in the transcript
    name_assign.update({old_name: f"CAND_{idx}" for idx, old_name in enumerate(old_speakers, 1)})
    return name_assign

def main():
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Parsing the input XML file")
    doctree = ET.parse(sys.stdin)
    text_elem = doctree.find(".//text")

    # sorting utterances by their start times
    u_elems_sorted = sorted(text_elem.findall("./u"), key=lambda elem: float(elem.get("start")))

    # guessing speaker roles to rename the speakers
    speaker_roles = guess_speaker_roles(u_elems_sorted)
    
    # clear all the utterances
    text_elem.clear()

    # insert them back sorted
    for idx, u_elem in enumerate(u_elems_sorted, 1):
        # remove other than specified attributes
        for attr_name in u_elem.keys():
            if attr_name not in ["start", "end", "who"]:
                del u_elem.attrib[attr_name]
        # set standard names for speakers, guessing the examiner by the content
        u_elem.attrib["who"] = speaker_roles[u_elem.attrib["who"]]
        # re-index IDs
        u_elem.attrib["id"] = f"u-{idx}"
        text_elem.append(u_elem)

    logging.debug("Printing the output XML file")
    doctree.write(sys.stdout, encoding="unicode", xml_declaration=True)

if __name__ == "__main__":
    main()
