"""List parameters and commands for FFMPEG to keep only a single speaker.

Given an XML transcript, it extracts names of all speakers and timestamps of all their utterances.
For each speaker, it outputs the FFMPEG parameters and commands to keep just the speaker in the recording.
Each line represents one speaker with the name of the speaker and the FFMPEG command tab-delimited.
"""
import argparse
import sys
import xml.etree.ElementTree as ET

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_xml", type=str, help="Input XML as a source of speakers and time segments.")
    parser.add_argument("--delete", action="store_true", help="Delete the segments that do not belong to the specified speaker. Otherwise, mute them.")
    parser.add_argument("--join-neighbours", action="store_true", help="Joins neighbouring segments of the same speakers.")
    args = parser.parse_args()
    return args

def join_neighbouring_segments(speaker_times):
    new_speaker_times = []
    prev_speaker = None
    new_start, new_end = None, None
    for speaker, start, end in speaker_times:
        if prev_speaker is not None and speaker != prev_speaker:
            new_speaker_times.append((prev_speaker, new_start, new_end))
            new_start = start
        if new_start is None:
            new_start = start
        new_end = end
        prev_speaker = speaker
    new_speaker_times.append((prev_speaker, new_start, new_end))
    return new_speaker_times

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

def main():
    args = parseargs()

    # read the input XML and extract a (speaker, start_time, end_time) tuple for each utterance
    doctree = ET.parse(args.input_xml)
    text_elem = doctree.find(".//text")
    all_speaker_times = [(u_elem.attrib['who'], u_elem.attrib['start'], u_elem.attrib['end']) for u_elem in text_elem.findall("./u")]

    # join neighbouring segments of the same speaker
    if args.join_neighbours:
        all_speaker_times = join_neighbouring_segments(all_speaker_times)

    # output for a speaker per line
    all_speakers = sorted(set([speaker for speaker, _, _ in all_speaker_times]))
    for speaker in all_speakers:
        speaker_times = [(start, end) for speaker1, start, end in all_speaker_times if speaker1 == speaker]
        # delete all except for the selected time segments
        if args.delete:
            ffmpeg_cmd = delete_outside_segments_cmd(speaker_times)
        # mute all except for the selected time segments
        else:
            ffmpeg_cmd = mute_outside_segments_cmd(speaker_times)
        print(speaker + "\t" + ffmpeg_cmd)

if __name__ == "__main__":
    main()
