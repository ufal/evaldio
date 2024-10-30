import argparse
import json
import h5py
import torch
import os

from torch.utils.data import DataLoader
import tqdm
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

from audio_classification_dataset import AudioClassificationDataset

def collate_fn(batch):
    ids, audio, _ = zip(*batch)
    return ids, audio

def main(args):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = args.model_id

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    model.eval()

    processor = AutoProcessor.from_pretrained(model_id)

    dataset = AudioClassificationDataset(
        args.datalists,
        args.h5_file,
        attributes=[],
    )

    dataloader = DataLoader(dataset, batch_size=args.batch_size, num_workers=args.num_workers, shuffle=False, collate_fn=collate_fn)

    model_args = {
        "language": "czech",
        "task": "transcribe",
        "num_beams": args.num_beams,
    }

    h5_file = args.h5_file.replace(".h5", f"+{model_id.replace('/', '-')}.h5")
    with h5py.File(args.h5_file, "r") as r:
        with h5py.File(h5_file, "w") as f:
            data = json.loads(r.attrs['dataset'])

            for batch in tqdm.tqdm(dataloader):
                audio = batch[1]
                audio = processor(audio, return_tensors="pt", sampling_rate=16000, return_attention_mask=True, device=device)
                audio = {k: v.to(device).to(torch_dtype) for k, v in audio.items()}

                transcripts = model.generate(**audio, **model_args)
                transcripts = processor.batch_decode(transcripts, skip_special_tokens=True)
                for id, transcript in zip(batch[0], transcripts):
                    data[id]['TRANSCRIPT'] = transcript
                    # print(f"{id}: {transcript}")

            f.attrs['dataset'] = json.dumps(data, ensure_ascii=False)
            for key, value in r.items():
                f.create_dataset(key, data=value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--h5_file", type=str, required=True)
    parser.add_argument("--datalists", type=str, nargs="+", required=True)
    parser.add_argument("--model_id", type=str, default="openai/whisper-large-v3")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--num_beams", type=int, default=4)
    parser.add_argument("--num_workers", type=int, default=4)
    args = parser.parse_args()

    main(args)