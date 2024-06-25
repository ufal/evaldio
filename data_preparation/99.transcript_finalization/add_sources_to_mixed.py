"""Add source system information to the mixed transcripts.

Some transcripts have been mixed from multiple ASR systems 
before they were post-edited by the human annotators.
Since annotators should not know which utterance is coming
from which system, the information on source systems have
not been added to the input for the annotators.

However, it can be helpful to have such information in the transcripts.
We therefore put this information back to each 'u' element as
the 'source' attribute.
"""
import argparse
import logging
import sys
import xml.etree.ElementTree as ET

def parse_logfile(logfile_path):
    uid2source = {}
    with open(logfile_path, "r") as logfile:
       for line in logfile:
           line = line.rstrip()
           if "selected from" not in line:
               continue
           uid = line.split(":")[2].split(" ")[0]
           source_system = line.split("/")[-2]
           uid2source[uid] = source_system
    return uid2source

def main():
    # Configure the logging module
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Script to add source system information to the transcripts mixed from multiple ASR systems.")
    parser.add_argument('logfile')
    args = parser.parse_args()

    uid2source = parse_logfile(args.logfile)

    logging.debug("Parsing the input XML file")
    doctree = ET.parse(sys.stdin)
    text_elem = doctree.find(".//text")

    u_elems = text_elem.findall("./u")
    for u_elem in u_elems:
        uid = u_elem.attrib["id"]
        u_elem.attrib["source"] = uid2source[uid]

    logging.debug("Printing the output XML file")
    doctree.write(sys.stdout, encoding="unicode", xml_declaration=True)

if __name__ == "__main__":
    main()
