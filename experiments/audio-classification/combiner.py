import argparse
import json
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

KEY = "filename"

def load_file(file_name):
    lines = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line = json.loads(line)
            lines.append(line)
    return lines

def default_pred(line, attr):
    line = dict(line)
    line[attr] = {attr_name: 0 for attr_name in line[attr].keys()}
    return line

def argmax_pred(line, attr):
    line = dict(line)
    k,v = list(line[attr].keys()), list(line[attr].values())
    max_idx = v.index(max(v))
    line[attr] = k[max_idx]
    return line

def argmax(line, attr):
    line = dict(line)
    k,v = list(line[attr].keys()), list(line[attr].values())
    max_idx = v.index(max(v))
    line[attr] = {attr_name: 0 for attr_name in line[attr].keys()}
    line[attr][k[max_idx]] = 1
    return line

def predict(lines, attr):
    predictions = {}

    for line in lines:
        key = line[KEY]
        pred = predictions.get(key, default_pred(line, attr))
        pred[attr] = {k: v + pred[attr].get(k, 0) for k,v in line[attr].items()}
        predictions[key] = pred
    
    for key, pred in predictions.items():
        predictions[key][attr + '+prob'] = predictions[key][attr]
        predictions[key] = argmax_pred(pred, attr)
    return predictions

def print_eval(predictions, truths, figure_file):

    report = classification_report(truths, predictions, output_dict=False)
    print(report)

    labels = sorted(list(set(truths)))
    cm = confusion_matrix(truths, predictions)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, xticklabels=labels, yticklabels=labels, fmt='d', cmap='Blues', cbar=False)#, mask=mask)

    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.savefig(figure_file, format="pdf", bbox_inches='tight')


def main(args):
    lines = []
    for file_name in args.input_files:
        lines.extend(load_file(file_name))

    predictions = predict(lines, args.attribute)

    for line in predictions.values():
        if line[args.attribute.replace("-predicted", "")] != line[args.attribute] and line[args.attribute.replace("-predicted", "")] != 'EXAM':
            print(line)

    truths = [line[args.attribute.replace("-predicted", "")] for line in predictions.values()]
    predictions = [line[args.attribute] for line in predictions.values()]
    print_eval(predictions, truths, args.confusion_matrix)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_files", type=str, nargs="+", required=True)
    parser.add_argument("--attribute", type=str, required=True)
    parser.add_argument("--confusion_matrix", type=str, default="confusion_matrix.pdf")
    args = parser.parse_args()
    main(args)