import glob
import os
import argparse
import numpy as np
import h5py
import torch
import tqdm
import torchaudio
import json

def load_audio(file_path, sample_rate):
    waveform, sr = torchaudio.load(file_path)
    if waveform.size(0) > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sr != sample_rate:
        waveform = torchaudio.transforms.Resample(sr, sample_rate)(waveform)
    return waveform

def prepare_dataset(datalist, audio_dir, output_file, sample_rate, duration, min_duration, version, use_examiner, shuffle_segments):
    with open(datalist, 'r') as f:
        lines = f.readlines()

    spk_type = '*' if use_examiner else 'CAND'

    dataset = []
    step_duration = int(sample_rate * duration)

    header = None
    with h5py.File(output_file, 'w') as f:
        for idx, line in tqdm.tqdm(enumerate(lines), total=len(lines)):
            line = line.strip()
            if not line:
                continue
            if idx == 0:
                header = line.split()
                continue
            values = line.split()
            key = values[0]
            
            wildcard = os.path.join(audio_dir, f'{key}.{version}.speaker-{spk_type}_*.*')
            for file in glob.glob(wildcard):
                waveform = load_audio(file, sample_rate)
                filename = os.path.basename(file)

                if shuffle_segments > 0:
                    new_waveform = waveform.clone()
                    num_segments = int(np.floor(waveform.size(1) / shuffle_segments))
                    permutation = np.random.permutation(num_segments)
                    for idx, p in enumerate(permutation):
                        # print(f'{idx} -> {p}')
                        new_waveform[:, idx * shuffle_segments:(idx + 1) * shuffle_segments] = waveform[:, p * shuffle_segments:(p + 1) * shuffle_segments]
                    waveform = new_waveform

                f.create_dataset(filename, data=waveform.numpy())
                for i in range(0, waveform.size(1), step_duration):
                    if i + step_duration > waveform.size(1) and i + step_duration - waveform.size(1) < min_duration:
                        break
                    dataset.append({
                        'key': key,
                        'filename': filename,
                        'begin': i,
                        'end': min(i + step_duration, waveform.size(1)),
                        **{k: v for k, v in zip(header, values)},
                    })
                    dataset[-1]['IS_EXAMINER'] = 1 if 'EXAM' in filename else 0

        dataset = json.dumps(dataset, ensure_ascii=False)
        f.attrs['dataset'] = dataset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datalist', type=str)
    parser.add_argument('audio_dir', type=str)
    parser.add_argument('output_dir', type=str)
    parser.add_argument('--sample-rate', type=int, default=16000)
    parser.add_argument('--version', type=str, default='deleted')
    parser.add_argument('--use-examiner', action='store_true')
    parser.add_argument('--duration', type=float, default=20.0)
    parser.add_argument('--min-duration', type=float, default=10.0)
    parser.add_argument('--shuffle_segments', type=float, default=0.0)
    args = parser.parse_args()

    output_file = f'v_{args.version}+sr_{args.sample_rate}+dur_{args.duration}+min_dur_{args.min_duration}+ex_{args.use_examiner}+shuf_{args.shuffle_segments}.h5'
    output_file = os.path.join(args.output_dir, output_file)

    shuffle_segments = int(args.shuffle_segments) if args.shuffle_segments > 0 else 0
    shuffle_segments = shuffle_segments * args.sample_rate

    prepare_dataset(args.datalist, args.audio_dir, output_file, args.sample_rate, args.duration, args.min_duration, args.version, args.use_examiner, shuffle_segments)