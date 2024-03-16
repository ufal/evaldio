import json
import argparse
import os.path
import sys


def get_header(audio_filename):
    return f"""
<teiHeader>
    <recordingStmt>
      <recording>
        <media url="{audio_filename}"/>
      </recording>
    </recordingStmt>
</teiHeader>
"""

def get_utterance(i, data):
    if 'speaker' in data:
        speaker = data['speaker'] 
    else:
        print(f"Speaker not defined for utterance no. {i}", file=sys.stderr)
        speaker = "SPEAKER_00"
    return f"""<u n="{i}" start="{data['start']}" end="{data['end']}" id="u-{i}" who="{speaker}">{data['text']}</u>"""

parser = argparse.ArgumentParser()
parser.add_argument("input_json", type=str, help="Input JSON as output by WhisperX")
args = parser.parse_args()

with open(args.input_json, "r") as f:
    data = json.load(f)

print('<?xml version="1.0" encoding="UTF-8"?>')
print("<TEI>")

audio_filename = ".".join(os.path.basename(args.input_json).split(".")[:-1]) + ".mp3"
print(get_header(audio_filename))

print("<text>")

for i, seg in enumerate(data["segments"], 1):
    print(get_utterance(i, seg))

print("</text>")
print("</TEI>")
