
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns

def print_eval(predictions, truths, figure_file):

    report = classification_report(truths, predictions, output_dict=False)
    print(report)

    labels = sorted(list(set(truths)))
    cm = confusion_matrix(truths, predictions)
    tle, tue, ne, te = 0, 0, 0, 0
    true = 0
    for i, c in enumerate(cm[:-1,:-1]):
        lower_error = sum(c[:i] + [0,])
        upper_error = sum(c[i+1:] + [0,])
        tle += lower_error
        tue += upper_error
        neigh_error = (c[i + 1] if i + 1 < len(c) else 0) + (c[i - 1] if i - 1 >= 0 else 0)  
        total_error = sum(c) - c[i]
        ne += neigh_error
        te += total_error
        true += c[i]
        # print (labels[i], c[i], lower_error, upper_error, upper_error / (lower_error + upper_error))
    print(tle, tue, tue / (tle + tue))
    print(ne, te, ne / (te))
    true_exam = cm[-1][-1]
    missed_exam = sum(cm[-1][:-1]) + sum(cm[-1][:-1])
    total_true = true + true_exam
    total_missed = tle + tue + ne + te + missed_exam
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, xticklabels=labels, yticklabels=labels, fmt='d', cmap='Blues', cbar=False)#, mask=mask)

    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.savefig(figure_file, format="pdf", bbox_inches='tight')

if __name__ == '__main__':
    predictions = []
    truths = []
    with open("output.txt") as f:
        for line in f:
            line = line.strip().split("\t")
            predictions.append(line[2])
            truths.append(line[1])
    print_eval(predictions, truths, "confusion_matrix.pdf")