import glob
import os
import argparse
import random
import numpy as np
import h5py
import torch
import tqdm
import torchaudio
import json
import xml.etree.ElementTree as ET

def load_audio(file_path, sample_rate):
    waveform, sr = torchaudio.load(file_path)
    if waveform.size(0) > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sr != sample_rate:
        waveform = torchaudio.transforms.Resample(sr, sample_rate)(waveform)
    return waveform

def load_labels(file_path):
    exams = dict()
    for file in os.listdir(file_path):
        if file.endswith('.json'):
            name = file.replace('.json', '')
            with open(os.path.join(file_path, file), 'r') as f:
                exams[name] = json.load(f)
    return exams

def parse_transcript(file_path):
    dialog_acts = []
    tree = ET.parse(file_path)
    # read all elements u
    for elem in tree.iter():
        if elem.tag == 'u':
            dialog_acts.append({
                "start": elem.attrib['start'],
                "end": elem.attrib['end'],
                "speaker": elem.attrib['who'],
            })
    return dialog_acts

def load_transcripts(file_path):
    transcripts = dict()
    for file in os.listdir(file_path):
        if file.endswith('.xml'):
            name = file.replace('.xml', '')
            with open(os.path.join(file_path, file), 'r') as f:
                transcripts[name] = f.read()

def load_all(transcript_path, label_path):
    labels = dict()
    for file in os.listdir(label_path):
        if file.endswith('.json'):
            name = file.replace('.json', '')
            with open(os.path.join(label_path, file), 'r') as f:
                labels[name] = json.load(f)
    transcripts = dict()
    for file in os.listdir(transcript_path):
        if file.endswith('.xml'):
            name = file.replace('.xml', '')
            transcripts[name] = parse_transcript(os.path.join(transcript_path, file))
    assert len(transcripts) == len(labels), f'Number of transcripts and labels do not match: {len(transcripts)} != {len(labels)}'
    for key in transcripts.keys():
        labels[key]['transcript'] = transcripts[key]
    return labels

def split_speaker_transcripts(transcripts, min_duration, max_duration):
    splits = [[]]
    for turn in transcripts:
        turn_duration = float(turn['end']) - float(turn['start'])
        current_split = splits[-1]
        current_split_duration = float(current_split[-1]['end']) - float(current_split[0]['start']) if current_split else 0
        if current_split and current_split_duration + turn_duration >= max_duration:
            splits.append([])
            current_split = splits[-1]
        current_split.append(turn)
    return [ split for split in splits if any(map(lambda t: 'CAND' in t['speaker'], split)) ]

def prepare_audio_dataset(labels, audio_dir, output_file, sample_rate):
    with h5py.File(output_file, 'w') as f:
        for idx, (spk_name, label) in tqdm.tqdm(enumerate(labels.items()), total=len(labels)):
            audio_path = os.path.join(audio_dir, spk_name + '.mp3')
            waveform = load_audio(audio_path, sample_rate)
            f.create_dataset(spk_name, data=waveform.numpy())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label_path', type=str)
    parser.add_argument('transcript_path', type=str)
    parser.add_argument('audio_dir', type=str)
    parser.add_argument('output_dir', type=str)
    parser.add_argument('--sample-rate', type=int, default=16000)
    parser.add_argument('--use-examiner', action='store_true')
    parser.add_argument('--max-duration', type=float, default=20.0)
    parser.add_argument('--min-duration', type=float, default=5.0)
    args = parser.parse_args()

    output_file = f'sr_{args.sample_rate}+dur_{args.max_duration}+min_{args.min_duration}+exam_{args.use_examiner}.h5'
    output_file = os.path.join(args.output_dir, output_file)
    os.makedirs(args.output_dir, exist_ok=True)
    labels = load_all(args.transcript_path, args.label_path)
    for label in labels.values():
        label['transcript'] = split_speaker_transcripts(label['transcript'], args.min_duration, args.max_duration)
    num_labels = len(labels)
    labels = {k: v for k, v in labels.items() if len(v['transcript']) > 0}
    print(f'Number of labels: {num_labels} -> {len(labels)}')

    prepare_audio_dataset(labels, args.audio_dir, output_file, args.sample_rate)

    with open(os.path.join(args.output_dir, 'labels.json'), 'w') as f:
        l = [k for k in labels.keys()]
        random.shuffle(l)
        labels = {k: labels[k] for k in l}
        json.dump(labels, f, ensure_ascii=False, indent=4)