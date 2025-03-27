import argparse
import pandas

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('labels_csv', type=str, help='The path to the CSV file containing the labels for the old exams')
parser.add_argument('output_dir', type=str, help='The directory to output the JSON files to')
args = parser.parse_args()

COLUMN_NAMES = [
    'exam_id',
    'evaluator_id',
    'ex1_response',
    'ex1_lexical',
    'ex1_grammar',
    'ex2_response',
    'ex2_questions',
    'ex2_lexical',
    'ex2_grammar',
    'ex12_phoninter',
    'total_score',
    'total_percentage',
]

# Load the data from the CSV file
data = pandas.read_csv(args.labels_csv, sep="\t", names=COLUMN_NAMES, header=0)

# transform the total_percentage to a float
data['total_percentage'] = data['total_percentage'].str.replace('%', '').astype(float)/100

# append a new column with a boolean value indicating if the candidate passed the exam (total_percentage >= 0.6)
data['result'] = data['total_percentage'] >= 0.6

# Output each row to a separate JSON file in the output directory
for index, row in data.iterrows():
    print(row)
    output_file = f'{args.output_dir}/{row["exam_id"]}_anonym_audio.json'
    with open(output_file, 'w') as f:
        f.write(row.to_json())

