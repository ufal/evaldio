import argparse
import json
import pandas as pd
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Collect JSONs from a directory")
    parser.add_argument("json_dir", type=str, help="Directory with JSON files")
    parser.add_argument("output_tsv", type=str, help="Output TSV file")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # collect all JSONs in the directory into a list
    json_files = [f for f in os.listdir(args.json_dir) if f.endswith('.json')]
    data_list = [json.load(open(os.path.join(args.json_dir, f))) for f in json_files]
    for data in data_list:
        # remove "evaluations" key
        data.pop("evaluations", None)

    df = pd.json_normalize(data_list, meta=["exam_id", "avg"])
    df = df.drop_duplicates()
    df.to_csv(args.output_tsv, sep="\t", index=False)

if __name__ == "__main__":
    main()