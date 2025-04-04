import argparse
import json
import pandas

CONFIG = {
    'A2_older': { 
        'column_names': ['exam_id', 'evaluator_id',
                 'ex1_response', 'ex1_lexical', 'ex1_grammar',
                 'ex2_response', 'ex2_questions', 'ex2_lexical', 'ex2_grammar',
                 'total_phoninter', 'total_score', 'total_percentage'],
        'header_rows': 1,
    },
    'A2': {
        'column_names': ['exam_origname', 'exam_id', 'evaluator_id',
           'ex1_selfdescr_score', 'ex1_eventdescr_score', 'ex1_lexgram_score',
           'ex2_imgdescr_score', 'ex2_response_score', 'ex2_lexgram_score',
           'ex3_questions_score', 'ex3_lexgram_score',
           'total_interact_score', 'total_cohesion_score', 'total_phonol_score', 'total_score'],
        'header_rows': 3,
    }
}


def process_data(data, exam_type):
    if exam_type == 'A2_older':
        # transform the total_percentage to a float
        data['total_percentage'] = data['total_percentage'].replace('%', '').astype(float)/100
        # append a new column with a boolean value indicating if the candidate passed the exam (total_percentage >= 0.6)
        data['result'] = data['total_percentage'] >= 0.6
        return

    # delete the "exam_origname" column
    data.drop(columns=['exam_origname'], inplace=True)
    # extract the first row which contains the maximum scores and remove it from the data
    max_scores = data.iloc[0]
    data.drop(index=0, inplace=True)
    # add new columns with percentage values calculated from the scores normalized to the maximum scores
    for key in data.columns:
        if not key.endswith('_score'):
            continue
        # calculate the percentage value
        new_key = key.replace('_score', '_perc')
        data[new_key] = data[key].astype(float) / max_scores[key]

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('labels_csv', type=str, help='The path to the CSV file containing the labels for the old exams')
parser.add_argument('output_dir', type=str, help='The directory to output the JSON files to')
parser.add_argument('--exam-type', type=str, default='A2_older', help='The type of exam to prepare the labels for')
args = parser.parse_args()


if args.exam_type not in CONFIG:
    print(f'Invalid exam type: {args.exam_type}')
    exit(1)

# Load the data from the CSV file
data = pandas.read_csv(args.labels_csv, sep="\t", names=CONFIG[args.exam_type]['column_names'], skiprows=CONFIG[args.exam_type]['header_rows'])

max_scores = process_data(data, args.exam_type)
print(max_scores)

# Group data by exam_id
grouped_data = data.groupby('exam_id')

# Output each row to a separate JSON file in the output directory
for exam_id, group in grouped_data:
    evaluations = []
    for _, row in group.iterrows():
        evaluation_dict = row.to_dict()

        evaluations.append(evaluation_dict)
    # Create the average evaluation dictionary by averaging the scores across all evaluations
    avg_evaluation = {}
    for key in group.columns:
        if key in ['evaluator_id', 'exam_id']:
            continue
        avg_evaluation[key] = group[key].mean()
    # Create the output dictionary
    out_dict = {
        'evaluations': evaluations,
        'avg': avg_evaluation,
    }
    output_file = f'{args.output_dir}/{exam_id}_anonym_audio.json'
    with open(output_file, 'w') as f:
        json.dump(out_dict, f, indent=4)

