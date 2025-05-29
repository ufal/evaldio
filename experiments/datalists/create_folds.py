import argparse
import pandas as pd
from sklearn.model_selection import StratifiedKFold

INPUT_COLUMNS = [
    "EXAM_ID", "EXAM_PART_ID", "LEVEL", "TRUTH_RES"
]

argparser = argparse.ArgumentParser()
argparser.add_argument("--input_tsv", type=str, default="../for_paper_2025/prompting_results.tsv", help="Input TSV table")
argparser.add_argument("-k", "--k-folds", type=int, default=10, help="Number of folds for cross-validation (default: 10)")
argparser.add_argument("--print-fold", type=int, default=None, help="Print the fold with the given number (default: None, do not print any fold)")
argparser.add_argument("--examid-overlap", action="store_true", help="If set, the exam ids in the same fold may overlap, i.e. exam parts of the same exam are not guaranteed to appear in the same fold")
args = argparser.parse_args()

if args.examid_overlap:
    raise NotImplementedError("The examid_overlap option is not implemented yet. Please use the default behavior where exam parts of the same exam are guaranteed to appear in the same fold.")

input_df = pd.read_csv(args.input_tsv, sep="\t")
# reduce the input_df to the columns we need for stratification
input_df = input_df[INPUT_COLUMNS].groupby("EXAM_PART_ID").first().reset_index()

# the folding should be done over the table grouped by "EXAM_ID" so different parts of the same exam recording do not end up in different folds
grouped_df = input_df.groupby("EXAM_ID").first().reset_index()
# take the "LEVEL"+"TRUTH_RES" columns as the target for stratification
grouped_df["TARGET"] = grouped_df["LEVEL"] + "_" + grouped_df["TRUTH_RES"].astype(str)
# create a StratifiedKFold object
skf = StratifiedKFold(n_splits=args.k_folds, shuffle=True, random_state=42)
# create a new column "fold" and fill it with -1
grouped_df["FOLD"] = -1
# iterate over the folds and assign the fold number to the "fold" column
for fold_number, (train_index, test_index) in enumerate(skf.split(grouped_df, grouped_df["TARGET"])):
    grouped_df.iloc[test_index, grouped_df.columns.get_loc("FOLD")] = fold_number
    #for idx in test_index:
    #    grouped_df.iloc[idx, "FOLD"] = fold_number
    # get the exam ids for the current fold
    #exam_ids = grouped_df.iloc[test_index]["EXAM_ID"].tolist()
    # assign the fold number to the "fold" column for the rows with the exam ids
    #input_df.loc[input_df["EXAM_ID"].isin(exam_ids), "FOLD"] = fold_number
# print the number of examples in each fold

# merge the fold information back to the original input_df
input_df = input_df.merge(grouped_df[["EXAM_ID", "FOLD"]], on="EXAM_ID", how="left")

#print(input_df.head())
#print(len(input_df))
#fold_counts = input_df["FOLD"].value_counts().sort_index()
#print("Number of examples in each fold:")
#print(fold_counts)

if args.print_fold is not None:
    # print the fold with the given number with no idx num and du not pad with spaces
    fold_df = input_df[input_df["FOLD"] == args.print_fold]
    print("\n".join(fold_df["EXAM_PART_ID"].to_list()))

