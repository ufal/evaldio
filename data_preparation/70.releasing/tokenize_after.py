import argparse
import json
import sys
import xml.etree.ElementTree as ET

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_xml', help='Path to the input XML file')
    return parser.parse_args()

def parse_udpipe_json(fh):
    # parse the fh as JSON and yield the tokenized lines in the "result" field
    udpipe_res = json.loads(fh.read())
    for line in udpipe_res["result"].rstrip().split('\n'):
        yield line.rstrip().split(' ')

def main():
    args = parse_args()
    tokenized_lines = list(parse_udpipe_json(sys.stdin))
    doctree = ET.parse(args.input_xml)
    # check if the number of utterances in the XML file matches the number of tokenized lines
    if len(doctree.findall('.//u')) != len(tokenized_lines):
        raise ValueError(f"Number of utterances in the XML file does not match the number of tokenized lines: {len(doctree.findall('.//u'))} vs. {len(tokenized_lines)}")
    i = 1
    for u_elem, tokens in zip(doctree.iterfind('.//u'), tokenized_lines):
        # replace the text of the u element with the tokenized text
        # each token is wrapped in the <tok> element
        inline_elems = [(elem.tag, elem.attrib) for elem in u_elem]
        attrs = {k: v for k, v in u_elem.attrib.items()}
        u_elem.clear()
        u_elem.attrib.update(attrs)
        for token in tokens:
            if token == 'SOMEELEMENT':
                tag, attrs = inline_elems.pop(0)
                elem = ET.SubElement(u_elem, tag, attrs)
                continue
            tok_elem = ET.SubElement(u_elem, 'tok', {'id': f"w-{i}"})
            tok_elem.text = token
            i += 1
    doctree.write(sys.stdout.buffer, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    main()