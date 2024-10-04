"""List parameters and commands for FFMPEG to keep only a single speaker.

Given an XML transcript, it extracts names of all speakers and timestamps of all their utterances.
For each speaker, it outputs the FFMPEG parameters and commands to keep just the speaker in the recording.
Each line represents one speaker with the name of the speaker and the FFMPEG command tab-delimited.
"""
import argparse
import sys
import xml.etree.ElementTree as ET

def mute_outside_segments_cmd(time_segments):
    fields = []
    fields.append(f"volume=enable='lt(t,{time_segments[0][0]})':volume=0")
    for i in range(len(time_segments)-1):
        fields.append(f"volume=enable='between(t,{time_segments[i][1]},{time_segments[i+1][0]})':volume=0")
    fields.append(f"volume=enable='gt(t,{time_segments[len(time_segments)-1][1]})':volume=0")
    return f'-af "{", ".join(fields)}"'

def delete_outside_segments_cmd(time_segments):
    select_cmds = "; ".join(f"[0:a]atrim={seg[0]}:{seg[1]},asetpts=PTS-STARTPTS[a{i}]" for i, seg in enumerate(time_segments, 1))
    concat_cmd = "".join(f"[a{i+1}]" for i in range(len(time_segments))) + f"concat=n={len(time_segments)}:v=0:a=1[out]"
    return f'-filter_complex "{select_cmds}; {concat_cmd}" -map "[out]"'

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_xml", type=str, help="Input XML as a source of speakers and time segments")
    parser.add_argument("--delete", action="store_true", help="Delete the segments that do not belong to the specified speaker. Otherwise, mute them.")
    args = parser.parse_args()
    return args

def main():
    args = parseargs()
    doctree = ET.parse(args.input_xml)
    text_elem = doctree.find(".//text")
    # sorting utterances by their start times
    all_speakers = sorted(set([u_elem.attrib["who"] for u_elem in text_elem.findall("./u")]))
    for speaker in all_speakers:
        speaker_times = [(u_elem.attrib['start'], u_elem.attrib['end']) for u_elem in text_elem.findall("./u") if u_elem.attrib["who"] == speaker]
        if args.delete:
            ffmpeg_cmd = delete_outside_segments_cmd(speaker_times)
        else:
            ffmpeg_cmd = mute_outside_segments_cmd(speaker_times)
        print(speaker + "\t" + ffmpeg_cmd)

if __name__ == "__main__":
    main()
