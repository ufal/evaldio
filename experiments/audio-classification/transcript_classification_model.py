from typing import List
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl

from transformers import AutoModel


class TranscriptClassificationModel(pl.LightningModule):
    def __init__(self, hf_model: str, num_classes: List[int], r_drop: float = 0.0, lr: float = 1e-4, class_names:List[str] = None, class_value_names: List[List[str]] = None, dropout: float = 0.1):
        super().__init__()
        self.model = AutoModel.from_pretrained(hf_model, hidden_dropout_prob=dropout, attention_probs_dropout_prob=dropout, classifier_dropout=dropout)
        self.hidden_size = self.model.config.hidden_size
        self.dropout = nn.Dropout(dropout)
        self.classifiers = nn.ModuleList(nn.Linear(self.hidden_size, classes) for classes in num_classes)
        self.has_attention_mask = True
        self.r_drop = r_drop
        self.lr = lr
        self.class_names = class_names
        self.class_value_names = class_value_names
        
        self.save_hyperparameters()

        self.outputs = [[] for _ in num_classes]
        self.truths = [[] for _ in num_classes]

    def forward(self, input_values, attention_mask=None):
        assert attention_mask is not None or not self.has_attention_mask
        output = self.model(input_values, attention_mask=attention_mask, output_hidden_states=True)
        output = self.dropout(output.hidden_states[-1][:, 0, :])
        return [
            classifier(output)
            for classifier in self.classifiers
        ]

    def __r_drop(self, p, q):
        pq = F.kl_div(F.log_softmax(p, dim=1), F.softmax(q, dim=1), reduction='batchmean')
        qp = F.kl_div(F.log_softmax(q, dim=1), F.softmax(p, dim=1), reduction='batchmean')
        return (pq + qp) / 2

    def __step(self, batch, step_name):
        features = batch[1]
        attention_mask = batch[2] if self.has_attention_mask else None
        labels = batch[3]

        logits = self(features, attention_mask)
        loss = 0.
        for idx, (logit, label) in enumerate(zip(logits, labels)):
            loss += F.cross_entropy(logit, label)
            if not self.training:
                self.outputs[idx].extend(logit.argmax(dim=1).detach().cpu().numpy())
                self.truths[idx].extend(label.detach().cpu().numpy())
            else:
                # log accuracy 
                correct = (logit.argmax(dim=1) == label).sum().item()
                total = len(label)
                self.log(f"{step_name}_class_{idx}_accuracy", correct / total, prog_bar=True)

        if self.r_drop > 0:
            logits2 = self(features, attention_mask)
            loss2 = 0.
            r_drop = 0.
            for logit, logit2, label in zip(logits, logits2, labels):
                loss2 += F.cross_entropy(logit2, label)
                r_drop += self.__r_drop(logit, logit2)

            self.log(f"{step_name}_r_drop_loss", r_drop, prog_bar=True)
            loss = (loss + loss2) / 2 
            self.log(f"{step_name}_ce_loss", loss, prog_bar=True)
            loss += self.r_drop * r_drop
            self.log(f"{step_name}_total_loss", loss, prog_bar=True)
        else:
            self.log(f"{step_name}_ce_loss", loss, prog_bar=True)
            
        return loss

    def training_step(self, batch, batch_idx):
        return self.__step(batch, "train")
    
    def validation_step(self, batch, batch_idx):
        return self.__step(batch, "val")
    
    def test_step(self, batch, batch_idx):
        return self.__step(batch, "test")
    
    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=self.lr)

    def __on_epoch_start(self):
        self.outputs = [[] for _ in self.classifiers]
        self.truths = [[] for _ in self.classifiers]

    def __on_epoch_end(self, step_name):
        if len(self.outputs) == 0:
            return
        predictions = np.array(self.outputs)
        truths = np.array(self.truths)

        try:
            from sklearn.metrics import classification_report
            for idx, (p, t) in enumerate(zip(predictions, truths)):
                class_name = idx
                if self.class_names is not None:
                    class_name = self.class_names[idx]
                report = classification_report(t, p, output_dict=False, target_names=self.class_value_names[idx] if self.class_value_names is not None else None)
                print(report)
                report = classification_report(t, p, output_dict=True, target_names=self.class_value_names[idx] if self.class_value_names is not None else None)
                for key, value in report.items():
                    if key == "accuracy":
                        self.log(f"{step_name}_class_{class_name}_accuracy", value, prog_bar=False)
                    else:
                        for metric, metric_value in value.items():
                            self.log(f"{step_name}_class_{class_name}_{key}_{metric}", metric_value, prog_bar=False)
        except:
            pass

    def on_validation_epoch_start(self):
        self.__on_epoch_start()

    def on_validation_epoch_end(self):
        self.__on_epoch_end("val")

    def on_test_epoch_start(self):
        self.__on_epoch_start()

    def on_test_epoch_end(self):
        self.__on_epoch_end("test")

    