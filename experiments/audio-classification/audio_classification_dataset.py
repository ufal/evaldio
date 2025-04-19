from collections import defaultdict
import json
import logging
from numpy import copy
import torch

from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from pytorch_lightning import LightningDataModule

from transformers import AutoFeatureExtractor

from typing import Dict, List, Set
import h5py


class AudioClassificationDataset(Dataset):
    def __init__(self, labels: Set[str], dataset: Dict, h5_file: str, attributes: List[str]):
        super().__init__()

        all_values = defaultdict(set)
        for item in dataset.values():
            for attr in attributes:
                item[attr] = str(item[attr])
                all_values[attr].add(item[attr])
        self.all_values = {
            key: {value: i for i, value in enumerate(sorted(values))} for key, values in all_values.items()
        }

        self.attributes = attributes
        dataset = {k:v for k, v in dataset.items() if k in labels}
        self.dataset = []
        for key, item in dataset.items():
            segments = item["segments"]
            for segment in segments:
                new_item = dict(item)
                del new_item["segments"]
                new_item["filename"] = key
                new_item["start"] = int(min(float(utt["start"]) * 16000 for utt in segment))
                new_item["end"] = int(max(float(utt["end"]) * 16000 for utt in segment))
                self.dataset.append(new_item)

        self.h5_file = h5py.File(h5_file, "r")



    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]

        attributes = []
        for attr in self.attributes:
            attributes.append(self.all_values[attr][item[attr]])

        begin, end = item["start"], item["end"]
        waveform = self.h5_file[item["filename"]][0,begin:end]
        return idx, waveform, attributes


class AudioClassificationModule(LightningDataModule):
    def __init__(
        self,
        dataset_file: str,
        num_folds: int,
        dev_fold: int,
        test_fold: int,
        h5_file: str,
        batch_size: int,
        num_workers: int,
        attributes: List[str],
        processor: AutoFeatureExtractor,
    ):
        super().__init__()
        
        with open(dataset_file, "r") as f:
            dataset = json.load(f)
        self.dataset = dataset

        ds_nums = list(dataset.keys())
        self.train_folds = [ds_nums[i] for i in range(len(dataset)) if i % num_folds != dev_fold and i % num_folds != test_fold]
        self.dev_folds = [ds_nums[i] for i in range(len(dataset)) if i % num_folds == dev_fold]
        self.test_folds = [ds_nums[i] for i in range(len(dataset)) if i % num_folds == test_fold]
        self.h5_file = h5_file
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.attributes = attributes
        self.processor = processor


    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            self.train_dataset = AudioClassificationDataset(
                labels=self.train_folds,
                dataset=self.dataset,
                h5_file=self.h5_file,
                attributes=self.attributes,
            )
        self.dev_dataset = AudioClassificationDataset(
            labels=self.dev_folds,
            dataset=self.dataset,
            h5_file=self.h5_file,
            attributes=self.attributes,
        )
        if stage == "test" or stage is None:
            self.test_dataset = AudioClassificationDataset(
                labels=self.test_folds,
                dataset=self.dataset,
                h5_file=self.h5_file,
                attributes=self.attributes,
            )

    def __collate_fn(self, batch):
        batch = list(zip(*batch)) 
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
