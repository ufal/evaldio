"""Normalization of the TEITOK annotated transcripts.

This scripts normalizes the annotated transcripts in the TEITOK format
coming from manual annotation.
The normalization includes:
    - sorting utterances by their start times
    - remove other attributes than "start", "end", and "who"
    - re-index IDs 
"""

import logging
import sys
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Parsing the input XML file")
    doctree = ET.parse(sys.stdin)
    text_elem = doctree.find(".//text")

    # sorting utterances by their start times
    u_elems_sorted = sorted(text_elem.findall("./u"), key=lambda elem: float(elem.get("start")))
    
    # clear all the utterances
    text_elem.clear()

    # insert them back sorted
    for idx, u_elem in enumerate(u_elems_sorted, 1):
        # remove other than specified attributes
        for attr_name in u_elem.keys():
            if attr_name not in ["start", "end", "who"]:
                del u_elem.attrib[attr_name]
        # re-index IDs
        u_elem.attrib["id"] = f"u-{idx}"
        text_elem.append(u_elem)

    logging.debug("Printing the output XML file")
    doctree.write(sys.stdout, encoding="unicode", xml_declaration=True)
