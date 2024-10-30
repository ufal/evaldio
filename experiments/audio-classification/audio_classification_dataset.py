from collections import defaultdict
import json
import logging
import torch

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from pytorch_lightning import LightningDataModule

from transformers import AutoFeatureExtractor

from typing import List
import h5py


class AudioClassificationDataset(Dataset):
    def __init__(self, folds: List[str], h5_file: str, attributes: List[str], return_transcript: bool = False, examiner_only: bool = False):
        super().__init__()

        self.attributes = attributes
        self.folds = folds
        self.return_transcript = return_transcript

        keys = set()
        for fold in folds:
            with open(fold, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    keys.add(line.split()[0])

        self.h5_file = h5py.File(h5_file, "r")

        dataset = json.loads(self.h5_file.attrs["dataset"])

        if examiner_only:
            dataset = [d for d in dataset if d["IS_EXAMINER"] == 1]
            logging.info(f"Examiner only: {len(dataset)}")
        else:
            for item in dataset:
                if item["IS_EXAMINER"]:
                    item["NORM_LEVEL"] = "EXAM"
                    item["HAS_RESIDENCE"] = "1"

        if return_transcript:
            dataset = [d for d in dataset if d["NORM_LEVEL"] != "EXAM"]

        all_values = defaultdict(set)
        for item in dataset:
            for attr in attributes:
                all_values[attr].add(item[attr])
        self.all_values = {
            key: {value: i for i, value in enumerate(sorted(values))} for key, values in all_values.items()
        }

        dataset = [d for d in dataset if d["key"] in keys]
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]

        attributes = []
        for attr in self.attributes:
            attributes.append(self.all_values[attr][item[attr]])

        if self.return_transcript:
            return idx, item["TRANSCRIPT"], attributes
        else:
            begin, end = item["begin"], item["end"]
            waveform = self.h5_file[item["filename"]][0,begin:end]
            return idx, waveform, attributes


class AudioClassificationModule(LightningDataModule):
    def __init__(
        self,
        train_folds: List[str],
        dev_folds: List[str],
        test_folds: List[str],
        h5_file: str,
        batch_size: int,
        num_workers: int,
        attributes: List[str],
        processor: AutoFeatureExtractor,
        return_transcript: bool = False,
        examiner_only: bool = False,
    ):
        super().__init__()
        
        for dt_fold in dev_folds + test_folds:
            train_folds = [f for f in train_folds if f != dt_fold]

        self.train_folds = train_folds
        self.dev_folds = dev_folds
        self.test_folds = test_folds
        self.h5_file = h5_file
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.attributes = attributes
        self.processor = processor
        self.return_transcript = return_transcript
        self.examiner_only = examiner_only

    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            self.train_dataset = AudioClassificationDataset(
                self.train_folds, self.h5_file, self.attributes, self.return_transcript, self.examiner_only
            )
            self.dev_dataset = AudioClassificationDataset(
                self.dev_folds, self.h5_file, self.attributes, self.return_transcript, self.examiner_only
            )
        if stage == "test" or stage == "predict" or stage is None:
            self.test_dataset = AudioClassificationDataset(
                self.test_folds, self.h5_file, self.attributes, self.return_transcript, self.examiner_only
            )

    def __collate_fn(self, batch):
        batch = list(zip(*batch)) 
        if self.return_transcript:
            output = self.processor(batch[1], return_attention_mask=True, padding=True, return_tensors="pt", max_length=512, truncation=True)
            features, attn_mask = output["input_ids"], output["attention_mask"]
        else:
            output = self.processor(batch[1], return_attention_mask=True, padding='longest', sampling_rate=16000, return_tensors="pt")
            features, attn_mask = output["input_values"], output["attention_mask"]
        attrs = [torch.tensor(a) for a in zip(*batch[2])]
        return batch[0], features, attn_mask, attrs

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            shuffle=True,
            collate_fn=self.__collate_fn,
        )

    def val_dataloader(self):
        return DataLoader(
            self.dev_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self.__collate_fn,
        )

    def test_dataloader(self):
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self.__collate_fn,
        )
    
    def predict_dataloader(self):
        return self.test_dataloader()
