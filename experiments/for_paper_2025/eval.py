import argparse
from collections import defaultdict
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
argparser.add_argument("--plot_thresholds", action="store_true", help="Plot thresholds for QWK optimization")
args = argparser.parse_args()

df = pd.read_csv(args.input_table, sep="\t")

if args.model_id:
    df = df[df["MODEL_ID"] == args.model_id]
if args.level:
    df = df[df["LEVEL"] == args.level]


def calc(df, col="PRED_RES", truth_col="TRUTH_RES"):
    # calculate precision, recall, f1-score, and support and print it below the plot
    truths = df[truth_col].tolist()
    predictions = df[col].tolist()
    print(f"Evaluating {len(truths)} samples...")
    print(f"predictions: {sum(predictions)}")
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

calc(df, col="PRED_RES", truth_col="TRUTH_RES")

thresh_qwk = defaultdict(list)
best_thresholds = defaultdict(lambda: 0.5)  # Default threshold for binary classification
# Optimize threshold to maximize QWK if probability scores are available
if args.plot_thresholds and "PRED_PERC" in df.columns:
    for level in sorted(df["LEVEL"].unique()):
        level_df = df[df["LEVEL"] == level]
        best_threshold, best_qwk = 0, 0
        for threshold in range(0, 101, 1):
            threshold /= 100.0
            preds = (level_df["PRED_PERC"] >= threshold).astype(int).tolist()
            qwk = cohen_kappa_score(level_df["TRUTH_RES"], preds, weights='quadratic', labels=[0, 1])
            if qwk > best_qwk:
                best_qwk = qwk
                best_threshold = threshold
            best_thresholds[level] = best_threshold
            thresh_qwk[level].append(qwk)
    thresholds_qwk = pd.DataFrame(thresh_qwk)
    thresholds_qwk.to_csv(f"thresholds_qwk_{args.model_id}.csv", index=False)
    if args.plot_thresholds:
        import matplotlib.pyplot as plt
        for level in thresholds_qwk.columns:
            plt.plot([i/100.0 for i in range(0, 101, 1)], thresholds_qwk[level], label=level)
        plt.xlabel("Threshold")
        plt.ylabel("QWK")
        plt.title(f"QWK vs Threshold")
        plt.legend()
        plt.savefig(f"thresholds_qwk_{args.model_id}.png")
        plt.show()
    
    # Print the best thresholds for each level
    print("Best thresholds for each level:")
    for level, threshold in best_thresholds.items():
        print(f"{level}: {threshold:.2f}")

    # apply the best thresholds to predictions
    df["PRED_RES_BEST"] = df.apply(lambda row: 1 if row["PRED_PERC"] >= best_thresholds[row["LEVEL"]] else 0, axis=1)
    calc(df, col="PRED_RES_BEST", truth_col="TRUTH_RES")
