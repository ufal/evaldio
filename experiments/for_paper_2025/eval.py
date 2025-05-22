import argparse
import json
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score

argparser = argparse.ArgumentParser()
argparser.add_argument("--model-id", type=str, help="Filter by Model ID")
argparser.add_argument("--level", type=str, help="Filter by Level")
argparser.add_argument("--json", action="store_true", help="Output in JSON format")
argparser.add_argument("input_table", type=str, help="Input table")
args = argparser.parse_args()

df = pd.read_csv(args.input_table, sep="\t")

if args.model_id:
    df = df[df["MODEL_ID"] == args.model_id]
if args.level:
    df = df[df["LEVEL"] == args.level]



# calculate precision, recall, f1-score, and support and print it below the plot
truths = df["TRUTH_RES"].tolist()
predictions = df["PRED_RES"].tolist()
scores = precision_recall_fscore_support(truths, predictions, labels=[False, True], average=None)
confusion = confusion_matrix(truths, predictions, labels=[False, True])
qwk = cohen_kappa_score(truths, predictions, weights='quadratic', labels=[0, 1])

if args.json:
    output = {
        "precision": scores[0].tolist(),
        "recall": scores[1].tolist(),
        "f1-score": scores[2].tolist(),
        "support": scores[3].tolist(),
        "confusion_matrix": confusion.tolist(),
        "qwk": qwk,
    }
    print(json.dumps(output, indent=4))
else:
    print(f"Confusion matrix:\n{confusion}")
    print(f"Support: {scores[3][0]}   {scores[3][1]}")
    print(f"Precision: {scores[0][0]:.2f}   {scores[0][1]:.2f}")
    print(f"Recall: {scores[1][0]:.2f}   {scores[1][1]:.2f}")
    print(f"F1-score: {scores[2][0]:.2f}   {scores[2][1]:.2f}")
    print(f"QWK: {qwk:.2f}")