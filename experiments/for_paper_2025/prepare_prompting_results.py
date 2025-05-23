import pandas as pd

EXPERIMENT_PATHS = {
    "pass_fail": "../prompting/2025-04-09_prompting_v6/table_whisperX.tsv",
    "holistic_score": "../prompting/2025-04-23_prompting_v7/table_whisperX.tsv",
    "trait_scores": "../prompting/2025-04-29_prompting_v8/table_whisperX.tsv",
}

OUTPUT_PATH = "prompting_results.tsv"

OUTPUT_COLUMNS = [
    "EXAM_ID", "EXAM_PART_ID", "MODEL_ID", "LEVEL",
    "TRUTH_RES", "TRUTH_PERC",
    "PRED_RES", "PRED_PERC"
]

THRESHOLDS = {
    "A1": 0.47, "A2": 0.51, "A2_older": 0.6, "B1": 0.62, "B2": 0.62,
}

def transform_df(input_df, experiment):
    new_df = pd.DataFrame()
    new_df["EXAM_ID"] = input_df["exam_id"]
    new_df["EXAM_PART_ID"] = input_df["exam_part_id"]
    new_df["MODEL_ID"] = experiment + "." + input_df['modelid'] + ".rs=" + input_df['randseed'].astype(str)
    new_df["LEVEL"] = input_df["level"]
    new_df["TRUTH_RES"] = input_df["avg.etalon_perc"] >= input_df["level"].map(THRESHOLDS)
    new_df["TRUTH_PERC"] = input_df["avg.etalon_perc"]
    if experiment == "pass_fail":
        new_df["PRED_RES"] = input_df["prediction"]
    elif experiment == "holistic_score":
        new_df["PRED_PERC"] = input_df["pred.score"]/100
        new_df["PRED_RES"] = new_df["PRED_PERC"] >= input_df["level"].map(THRESHOLDS)
    elif experiment == "trait_scores":
        new_df["PRED_PERC"] = input_df["pred.total_score"]/100
        new_df["PRED_RES"] = new_df["PRED_PERC"] >= input_df["level"].map(THRESHOLDS)
    return new_df


if __name__ == "__main__":
    # read the input files
    new_merged_df = pd.DataFrame()
    for experiment, path in EXPERIMENT_PATHS.items():
        df = pd.read_csv(path, sep="\t")
        print(f"Read {experiment} data from {path}")
        # transform the data
        transformed_df = transform_df(df, experiment)
        print(f"Transformed {experiment} data")
        print(transformed_df.head())
        # merge the data
        new_merged_df = pd.concat([new_merged_df, transformed_df], ignore_index=True)
    # save the merged data
    new_merged_df = new_merged_df[OUTPUT_COLUMNS]
    new_merged_df.to_csv(OUTPUT_PATH, sep="\t", index=False)