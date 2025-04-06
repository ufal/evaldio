import argparse
import xml.etree.ElementTree as ET

argparser = argparse.ArgumentParser(description='Delete <autoFilter> elements from the XML files in the given directory.')
argparser.add_argument('input_xlsx', type=str, help='The input XLSX file to process')
argparser.add_argument('output_xlsx', type=str, help='The output XLSX file to process')
args = argparser.parse_args()

tree = ET.parse(args.input_xlsx)
root = tree.getroot()

# Remove all <autoFilter> elements
for af in root.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}autoFilter"):
    parent = af.getparent() if hasattr(af, "getparent") else None
    if parent is not None:
        parent.remove(af)
    else:
        root.remove(af)
ET.register_namespace('', "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
tree.write(args.output_xlsx, xml_declaration=True, encoding='UTF-8')