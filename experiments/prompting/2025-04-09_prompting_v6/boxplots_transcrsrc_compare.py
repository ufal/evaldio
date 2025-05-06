import argparse
import pandas as pd

from matplotlib import pyplot as plt
import seaborn as sns

THRESHOLDS = {
    "A1": 0.47, "A2": 0.51, "A2_older": 0.6, "B1": 0.62,
}

def parse_args():
    parser = argparse.ArgumentParser(description="Compare boxplots of predictions made on whisperX/manual transcripts.")
    parser.add_argument("manual_table_tsv", type=str, help="The TSV file with the predictions on manual transcripts")
    parser.add_argument("whisperX_table_tsv", type=str, help="The TSV file with the predictions on whisperX transcripts")
    parser.add_argument("--output-tsv", type=str, help="The output TSV file")
    parser.add_argument("--output-pdf", type=str, help="The output PDF file")
    args = parser.parse_args()
    return args

def read_inputs(manual_table_tsv, whisperX_table_tsv):
    merged_df = pd.DataFrame()
    
    manual_df = pd.read_csv(manual_table_tsv, sep="\t")
    manual_df["transcript_src"] = "manual"
    merged_df = pd.concat([merged_df, manual_df], ignore_index=True)

    whisperX_df = pd.read_csv(whisperX_table_tsv, sep="\t")
    whisperX_df["transcript_src"] = "whisperX"
    merged_df = pd.concat([merged_df, whisperX_df], ignore_index=True)

    return merged_df

def evaluate_and_plot_selected(ax, df, level=None, modelid=None, with_legend=False):
    # filter by modelid
    if modelid is not None:
        df = df[df["modelid"] == modelid]
    # filter by level and modelid
    if level is not None:
        df = df[df["level"] == level]

    # plot the boxplots
    sns.boxplot(x="avg.etalon_perc", y="prediction", hue="transcript_src", orient="y", order=[True, False], hue_order=["whisperX", "manual"], dodge=True, data=df, ax=ax)
    if level is not None and level in THRESHOLDS:
        # add a vertical line at the threshold
        ax.axvline(THRESHOLDS[level], color='red', linestyle='--')

    # remove the legend
    if not with_legend:
        ax.legend_.remove()

    # set the x axis limits
    ax.set_xlim(0, 1)
    
    # set the title and make it bold
    title = f"{modelid} - {level}" if level is not None else modelid
    ax.set_title(title, fontsize=14, fontweight='bold')
    

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
            with_legend = False
            # add legend to the first plot
            if i == 0 and j == 0:
                with_legend = True
            evaluate_and_plot_selected(axs[i, j], df, level=level, modelid=modelid, with_legend=with_legend)
    
    # save the figure
    fig.tight_layout()
    fig.savefig(output_file, format="pdf", bbox_inches='tight')

def main():
    args = parse_args()
    df = read_inputs(args.manual_table_tsv, args.whisperX_table_tsv)
    if args.output_tsv:
        df.to_csv(args.output_tsv, sep="\t", index=False)
    if args.output_pdf:
        evaluate_all(df, args.output_pdf)

if __name__ == "__main__":
    main()