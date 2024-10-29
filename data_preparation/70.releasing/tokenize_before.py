import sys
import xml.etree.ElementTree as ET

def main():
    doctree = ET.parse(sys.stdin)
    for elem in doctree.iterfind('.//u'):
        text = elem.text or ""
        for child in elem:
            text += "SOMEELEMENT"           
            text += child.tail or ""
        print(text)

if __name__ == '__main__':
    main()