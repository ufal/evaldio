import argparse
import os
import re
import shutil
import xml.etree.ElementTree as ET

def parse_args():
    parser = argparse.ArgumentParser(description='Rename recordings')
    parser.add_argument('input_files', type=str, nargs='+', help='Input files')
    parser.add_argument('output_dir', type=str, help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Do not write any files')
    parser.add_argument('--verbose', action='store_true', help='Print debug information')
    return parser.parse_args()

def change_basename_mp3(basename):
    match = re.match(r'(?P<level>[A-C][1-2])ML_(?P<rec_date>\d{6})_(?P<examno>\d{2}).*-exer(?P<exerno>[1-9])\.mp3', basename)
    return f'UJOP-{match.group("level")}-{match.group("rec_date")}_{match.group("examno")}-task{match.group("exerno")}.mp3'
    
def change_basename_other(basename):
    match = re.match(r'(?P<level>[A-C][1-2])ML_(?P<rec_date>\d{6})_(?P<examno>\d{2}).*-(?P<annotator_short>\w{2})-(?P<type>\w+)-exer(?P<exerno>[1-9])\.(?P<extension>\w+)', basename)
    return f'UJOP-{match.group("level")}-{match.group("rec_date")}_{match.group("examno")}-task{match.group("exerno")}-{match.group("type")}-{match.group("annotator_short")}.{match.group("extension")}'

def main():
    args = parse_args()
    for input_file in args.input_files:
        input_dir, input_base = os.path.split(input_file)
        
        # determine new name for the file
        output_base = None
        if input_base.endswith('.mp3'):
            output_base = change_basename_mp3(input_base)
        else:
            output_base = change_basename_other(input_base)

        # rename the reference to the recording in the annotation file
        tree = None
        if input_base.endswith('.xml'):
            tree = ET.parse(input_file)
            root = tree.getroot()
            for recording in root.findall('.//media'):
                recording.attrib["url"] = change_basename_mp3(recording.attrib["url"])
        
        # copy the file to the output directory
        output_file = os.path.join(args.output_dir, output_base)
        if not args.dry_run:
            if tree is not None:
                tree.write(output_file, encoding="utf-8", xml_declaration=True)
            else:
                shutil.copyfile(input_file, output_file)
        else:
            args.verbose = True
        if args.verbose:
            print(f"'{input_file}' -> '{output_file}'")

if __name__ == '__main__':
    main()