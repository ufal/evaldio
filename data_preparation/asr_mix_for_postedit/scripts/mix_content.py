#!/usr/bin/env python3

import argparse
import copy
import logging
import random
import sys
import xml.etree.ElementTree as ET

def select_xml_content(xml_files, fill_empty=False):
    # Parse the first XML file to get the teiHeadet
    first_tree = ET.parse(xml_files[0])
    tei_header = copy.deepcopy(first_tree.find(".//teiHeader"))

    # Create a new root element for the output XML
    output_root = ET.Element(first_tree.getroot().tag)
    output_root.append(tei_header)
    logging.debug(f"TEI header copied: {tei_header}")

    output_text_elem = ET.SubElement(output_root, 'text')
    u_elements = [ET.parse(xml_file).findall(".//text/u") for xml_file in xml_files]

    # Iterate through "u" elements and select the content
    for u_tuple in zip(*u_elements):
        uid = u_tuple[0].attrib["id"]
        if not all(u_elem.attrib["id"] == uid for u_elem in u_tuple):
            logging.error(f"Different 'u' elements: {u_tuple}")

        # Create a new "u" element for the output with a randomly selected content
        output_u_elem = copy.deepcopy(u_tuple[0])
        random_i = random.choice(range(len(u_tuple)))
        logging.info(f"{uid} selected from {xml_files[random_i]}")
        selected_text = u_tuple[random_i].text
        if fill_empty and not selected_text:
            selected_text = "???"
        output_u_elem.text = selected_text
        output_text_elem.append(output_u_elem)

    # Create an ElementTree from the output root and write it to STDOUT
    logging.debug(f"Printing the output XML file")
    output_tree = ET.ElementTree(output_root)
    output_tree.write(sys.stdout, encoding="unicode", xml_declaration=True)

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+", help="input documents")
parser.add_argument("--seed", type=str, default="2023", help="the string to initialize the random seed with")
parser.add_argument("--fill-empty", action="store_true", help="Fill empty utterances with ???")
args = parser.parse_args()

if __name__ == "__main__":
    # Configure the logging module
    logging.basicConfig(level=logging.INFO)
    logging.debug("Script started")

    # Setting the random seed
    random.seed(args.seed)

    # Randomly select the content and write the output XML to STDOUT
    select_xml_content(args.files, args.fill_empty)
