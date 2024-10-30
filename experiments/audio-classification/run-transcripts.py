import argparse

import pytorch_lightning as pl

from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import CSVLogger

from audio_classification_dataset import AudioClassificationModule
from transcript_classification_model import TranscriptClassificationModel
from transformers import AutoTokenizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir", type=str, default="runs")
    parser.add_argument("--train_folds", type=str, nargs="+", required=True)
    parser.add_argument("--dev_folds", type=str, nargs="+", required=True)
    parser.add_argument("--test_folds", type=str, nargs="+", required=True)
    parser.add_argument("--h5_file", type=str, required=True)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument(
        "--attributes", type=str, nargs="+", default=["NORM_LEVEL", "HAS_RESIDENCE"]
    )
    parser.add_argument("--max_epochs", type=int, default=1)
    parser.add_argument("--hf_model", type=str, default="ufal/robeczech-base")
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--r_drop", type=float, default=0.0)
    parser.add_argument("--accumulation_steps", type=int, default=1)
    parser.add_argument("--experiment_name", type=str, default=None)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    feature_extractor = AutoTokenizer.from_pretrained(args.hf_model)

    dataset = AudioClassificationModule(
        train_folds=args.train_folds,
        dev_folds=args.dev_folds,
        test_folds=args.test_folds,
        h5_file=args.h5_file,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        attributes=args.attributes,
        processor=feature_extractor,
        return_transcript=True,
    )
    dataset.setup('test')

    model = TranscriptClassificationModel(
        hf_model=args.hf_model,
        num_classes=[len(dataset.test_dataset.all_values[attr]) for attr in args.attributes],
        r_drop=args.r_drop,
        lr=args.lr,
        class_names=args.attributes,
        class_value_names=[list(dataset.test_dataset.all_values[attr].keys()) for attr in args.attributes],
        dropout=args.dropout,
    )

    checkpoint_callback = ModelCheckpoint(
        filename="classifier_{epoch:02d}",
        monitor="val_class_NORM_LEVEL_macro avg_f1-score",
        save_last=True,
        mode="max",
        save_top_k=1,
    )

    logger = CSVLogger(args.root_dir, name=args.experiment_name)

    trainer = pl.Trainer(
        max_epochs=args.max_epochs,
        callbacks=[checkpoint_callback],
        default_root_dir=args.root_dir,
        devices=1,
        accelerator="gpu",
        precision='16-mixed',
        logger=logger,
        accumulate_grad_batches=args.accumulation_steps,
    )
    trainer.fit(model, datamodule=dataset)

if __name__ == "__main__":
    main()
