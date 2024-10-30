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

EXAM_PATTERN_WEIGHTS = [
    (r"[Úú]lo[hz]", 10),
    (r"[Mm]inut", 10),
    (r"[Oo]táz[ek]", 5),
]

def filter_empty(u_elems):
    return [u_elem for u_elem in u_elems if u_elem.text]

def estimate_examiner_role(texts):
    pattern_counts = [
        sum([re.search(pattern, t) is not None for t in texts]) * weight
        for pattern, weight in EXAM_PATTERN_WEIGHTS
    ]
    score = (sum(pattern_counts) / len(texts)) / (sum(weight for _, weight in EXAM_PATTERN_WEIGHTS) * len(pattern_counts))
    return score

def normalize_speaker_roles(u_elems):
    for u_elem in u_elems:
        # remove potentially leading or trailing whitespace from old speaker names
        u_elem.attrib["who"] = u_elem.attrib["who"].strip()

def guess_speaker_role_by_name(u_elems):
    old_speakers = set([u_elem.attrib["who"] for u_elem in u_elems])
    # do not assign speaker roles by name if the speaker names have only numerical indices
    if all(re.match(r'^.*_\d\d$', speaker) for speaker in old_speakers):
        return None
    name_assign = {}
    # assign examiner roles
    exam_count = 0
    cand_count = 0
    for old_name in sorted(old_speakers):
        # EXAM roles to the speaker names that end with t*
        if re.match(r'^.*_t[^_]*$', old_name):
            name_assign[old_name] = f"EXAM_{exam_count+1}"
            exam_count += 1
        else:
            name_assign[old_name] = f"CAND_{cand_count+1}"
            cand_count += 1
    return name_assign

def guess_speaker_roles_by_content(u_elems):
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

def guess_speaker_roles(u_elems):
    # assign speaker roles
    # first try by name
    # if failed, assign by content
    name_assign = guess_speaker_role_by_name(u_elems)
    if name_assign:
        return name_assign
    return guess_speaker_roles_by_content(u_elems)

def main():
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Parsing the input XML file")
    doctree = ET.parse(sys.stdin)
    text_elem = doctree.find(".//text")

    u_elems = text_elem.findall("./u")
    
    # no normalization needed for empty transcripts
    if u_elems:

        # filter out empty utterances
        u_elems = filter_empty(u_elems)

        # sorting utterances by their start times
        u_elems_sorted = sorted(u_elems, key=lambda elem: float(elem.get("start")))

        # normalize speaker roles
        normalize_speaker_roles(u_elems_sorted)

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
