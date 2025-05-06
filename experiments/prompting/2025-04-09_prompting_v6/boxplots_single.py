import argparse
from collections import defaultdict
import pandas as pd

from matplotlib import pyplot as plt
#from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
import seaborn as sns

RESULT_FILE_DETAILS = {
    "header_randseeds_as_cols": ["level", "transcript_file", "truth", "prediction_42", "prediction_1986", "prediction_2025"],
    "header": ["level", "transcript_file", "truth", "randseed", "prediction"],
}
THRESHOLDS = {
    "A1": 0.47, "A2": 0.51, "A2_older": 0.6, "B1": 0.62,
}

def filename_to_examid(filename, with_partno=False):
    col_count = 3
    if with_partno:
        col_count = 4
    # for manually transcribed files
    if "from_" in filename:
        return "_".join(filename.split("-")[0].split("_")[:col_count])
    # for automatically transcribed files
    return "_".join(filename.split("_anonym")[0].split("_")[:col_count])

def read_inputs(files, randseeds_as_cols=False):
    df = pd.DataFrame()
    for file in files:
        df1 = pd.read_csv(
            file, 
            sep="\t",
            names=(RESULT_FILE_DETAILS["header"] if not randseeds_as_cols else RESULT_FILE_DETAILS["header_randseeds_as_cols"]),
            header=None
        )

        # remove the "truth" column, its values are no longer valid
        df1 = df1.drop(columns=["truth"])
        
        # add the modelid column
        modelid = file.split("/")[-1].split(".")[0]
        df1["modelid"] = modelid
        # add the examid column using the transcript_file column
        df1["exam_id"] = df1["transcript_file"].apply(filename_to_examid)
        # add the exampartid column using the transcript_file column
        df1["exam_part_id"] = df1["transcript_file"].apply(filename_to_examid, with_partno=True)
        
        if randseeds_as_cols:
            # melt the df1 to long format
            df1 = df1.melt(id_vars=["transcript_file", "exam_id", "exam_part_id", "level", "modelid"], var_name="randseed", value_name="prediction")
            # remove the prefix 'prediction_' from the randseed column
            df1["randseed"] = df1["randseed"].str.replace("prediction_", "")
        # append df1 to df
        df = pd.concat([df, df1], ignore_index=True)
    return df

def read_datalist(datalist_path):
    df = pd.read_csv(datalist_path, sep="\t")
    # add the exam_part_id column using the EXAM_ID column
    df["exam_part_id"] = df["EXAM_ID"].apply(filename_to_examid, with_partno=True)
    return df["exam_part_id"].tolist()

def read_labels(exam_labels_paths):
    df_labels = pd.DataFrame()
    for exam_labels_path in exam_labels_paths:
        df_labels1 = pd.read_csv(exam_labels_path, sep="\t")
        df_labels = pd.concat([df_labels, df_labels1], ignore_index=True)
    return df_labels

def evaluate_and_plot_selected(ax, df, level=None, modelid=None):
    # filter by modelid
    if modelid is not None:
        df = df[df["modelid"] == modelid]
    # filter by level and modelid
    if level is not None:
        df = df[df["level"] == level]

    # get the predictions and truths
    predictions = [str(x) for x in df["prediction"].tolist()]
    truths = df["avg.etalon_perc"].combine_first(df["avg.total_perc"]).tolist()
    data = {"truth": truths, "prediction": predictions}

    # plot the boxplot
    #sns.stripplot(x="truth", y="prediction", data=data, ax=ax, jitter=True, alpha=0.5)
    sns.boxplot(x="truth", y="prediction", order=["True", "False"], data=data, ax=ax, color='lightblue', fliersize=0, width=0.5)
    if level is not None and level in THRESHOLDS:
        # add a vertical line at the threshold
        ax.axvline(THRESHOLDS[level], color='red', linestyle='--')

    # set the x axis limits
    ax.set_xlim(0, 1)
    
    # set the title and make it bold
    title = f"{modelid} - {level}" if level is not None else modelid
    ax.set_title(title, fontsize=14, fontweight='bold')

    # calculate precision, recall, f1-score, and support and print it below the plot
    #scores = precision_recall_fscore_support(truths, predictions, average=None)
    #text = ''
    #for i, scorename in enumerate(['precision', 'recall', 'f1-score', 'support']):
    #    if scorename == 'support':
    #        text += f"{scorename}: {scores[i][0]}   {scores[i][1]}\n"
    #    else:
    #        text += f"{scorename}: {scores[i][0]:.2f}   {scores[i][1]:.2f}\n"
    #ax.text(0.5, -0.4, text, ha='center', va='center', transform=ax.transAxes)
    

def evaluate_all(df, output_file):
    # get levels, add all levels as None at the beginning
    levels = sorted(list(set(df["level"]))) + [None]
    # get modelids
    modelids = sorted(list(set(df["modelid"])))

    # create a len(modelids) x len(levels) pyplot canvas
    fig, axs = plt.subplots(len(levels), len(modelids), figsize=(15, 10))
    # set figsize
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    
    for i, level in enumerate(levels):
        for j, modelid in enumerate(modelids):
            evaluate_and_plot_selected(axs[i, j], df, level=level, modelid=modelid)
    
    # save the figure
    fig.tight_layout()
    fig.savefig(output_file, format="pdf", bbox_inches='tight')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate the LLM prompting outputs")
    parser.add_argument("--output-pdf", type=str, default="confmat.pdf", help="Confusion matrix output file")
    parser.add_argument("--output-tsv", type=str, default="table.tsv", help="Aggregated table the statistics is calculated from")
    parser.add_argument("--exam_labels_paths", nargs='+', help="Paths to the exam labels")
    parser.add_argument("--randseeds-as-cols", action="store_true", help="Use randseeds as columns")
    parser.add_argument("--datalist", type=str, help="Limit the evaluation to the given datalist")
    parser.add_argument("result_files", nargs='+', help="The result files to evaluate")
    args = parser.parse_args()

    # read the result files
    df = read_inputs(args.result_files, args.randseeds_as_cols)
    # aggregate the predictions produced by different seeds
    df = df.groupby(["level", "transcript_file", "modelid"]).agg(lambda x: x.mode()[0]).reset_index()

    # filter the df by datalist
    if args.datalist:
        datalist = read_datalist(args.datalist)
        df = df[df["exam_part_id"].isin(datalist)]
    
    # load the exam labels and join them with the predictions
    if args.exam_labels_paths:
        df_labels = read_labels(args.exam_labels_paths)
        df = df.merge(df_labels, on=["exam_id"], how="left")   

    # save the aggregated table to TSV
    if args.output_tsv:
        df.to_csv(args.output_tsv, sep="\t", index=False)

    # print the confusion matrices to PDF
    if args.output_pdf:
        evaluate_all(df, args.output_pdf)
    