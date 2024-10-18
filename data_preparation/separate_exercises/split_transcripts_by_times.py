"""Split the transcript in the TEITOK format at specified timestamps.
"""
import argparse
import copy
import logging
import sys
import xml.etree.ElementTree as ET

def parse_arguments():
    parser = argparse.ArgumentParser()
    #parser.add_argument("input_xml", type=str, help="Input transcript in the TEITOK format.")
    parser.add_argument("split_times", type=float, nargs='+', help="A list of timestamps at which the recording should be split.")
    parser.add_argument("--output-prefix", type=str, help="Path prefix to store the results of the split.")
    parser.add_argument("--part-name", type=str, default="part", help="Name of the part that is split.")
    args = parser.parse_args()
    return args

def belongs_to_split(u_elem, split_end_time):
    before_split_duration = split_end_time - float(u_elem.attrib["start"])
    after_split_duration = float(u_elem.attrib["end"]) - split_end_time
    return before_split_duration >= after_split_duration

def split_utterances_by_times(u_elems, times):
    sorted_times = sorted(times)
    is_distributed_list = [False] * len(u_elems)
    u_elem_splits = []
    # iterate over the end times of the splits and distribute the utterances to them
    prev_time = 0
    for time in sorted_times:
        u_elem_splits.append([])
        for i, u_elem in enumerate(u_elems):
            # skip utterances that have already been distributed
            if is_distributed_list[i]:
                continue
            # distribute the utterance to the current split if it is supposed to belong to it
            if belongs_to_split(u_elem, time):
                # adjust the utterance start and end times
                u_elem.attrib["start"] = "{:.3f}".format(max(float(u_elem.attrib["start"]) - prev_time, 0))
                u_elem.attrib["end"] = "{:.3f}".format(min(float(u_elem.attrib["end"]) - prev_time, time - prev_time))
                # add the utterance to the current split
                u_elem_splits[-1].append(u_elem)
                # mark the utterance as distributed
                is_distributed_list[i] = True
            else:
                break
        prev_time = time
    # distribute the remaining utterances to the last split
    u_elem_splits.append([])
    for i, u_elem in enumerate(u_elems):
        if not is_distributed_list[i]:
            # adjust the utterance start and end times
            u_elem.attrib["start"] = "{:.3f}".format(max(float(u_elem.attrib["start"]) - prev_time, 0))
            u_elem.attrib["end"] = "{:.3f}".format(float(u_elem.attrib["end"]) - prev_time)
            # add the utterance to the current split
            u_elem_splits[-1].append(u_elem)
    return u_elem_splits

def count_split_ratio(u_elems, u_elem_splits):
    split_ratio = []
    for u_elem_split in u_elem_splits:
        split_duration = sum(float(u_elem.attrib["end"]) - float(u_elem.attrib["start"]) for u_elem in u_elem_split)
        total_duration = sum(float(u_elem.attrib["end"]) - float(u_elem.attrib["start"]) for u_elem in u_elems)
        split_ratio.append(split_duration / total_duration)
    return split_ratio

def rename_media_path(doctree, part_name):
    media_elem = doctree.find(".//media")
    media_elem.attrib["url"] = f"{media_elem.attrib['url'][:-4]}.{part_name}.mp3"

def adjust_annotation_duration(doctree, split_ratio):
    annot_duration_elems = doctree.findall(".//annotDuration")
    logging.debug(f"Annot duration elements: {annot_duration_elems}")
    for annot_duration_elem in annot_duration_elems:
        new_duration = "{:.3f}".format(float(annot_duration_elem.text) * split_ratio)
        logging.debug(f"Changing the duration of the annotation from {annot_duration_elem.text} to {new_duration}.")
        annot_duration_elem.text = new_duration
        annot_duration_elem.attrib["approx"] = "1"

def replace_utt_elems(doctree, u_elem_split):
    text_elem_split = doctree.find(".//text")
    text_elem_split.clear()
    text_elem_split.extend(u_elem_split)

def main():
    args = parse_arguments()

    logging.basicConfig(level=logging.DEBUG)
        
    # parse the input XML file
    logging.info(f"Parsing the input XML file from stdin.")
    doctree = ET.parse(sys.stdin)
    text_elem = doctree.find(".//text")
    u_elems = text_elem.findall("./u")
    
    # split the utterances by the specified times
    logging.info(f"Splitting the transcript at times {args.split_times}.")
    u_elem_splits = split_utterances_by_times(u_elems, args.split_times)

    # count the split ratio
    split_ratio = count_split_ratio(u_elems, u_elem_splits)
    logging.debug(f"Split ratio: {split_ratio}")

    # deep-copy the original XML tree, replace the utterance elements, and write the new XML tree to the output directory
    for idx, u_elem_split in enumerate(u_elem_splits):
        doctree_split = copy.deepcopy(doctree)
        split_suffix = f"{args.part_name}{idx+1}"
        rename_media_path(doctree_split, split_suffix)
        adjust_annotation_duration(doctree_split, split_ratio[idx])
        replace_utt_elems(doctree_split, u_elem_split)
        logging.info(f"Writing the split transcript to {args.output_prefix}.{split_suffix}.xml")
        doctree_split.write(f"{args.output_prefix}.{split_suffix}.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
