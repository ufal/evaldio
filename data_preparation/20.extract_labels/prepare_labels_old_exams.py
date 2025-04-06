import argparse
import json
import os
import pandas

CONFIG = {
    'A1': {
        'column_names': ['exam_origname', 'exam_id', 'evaluator_id',
            'ex1_criterion1_score', 'ex1_criterion2_score', 'ex1_lexgram_score', 'ex1_phonol_score',
            'ex2_criterion1_score', 'ex2_criterion2_score', 'ex2_socling_score', 'ex2_lexgram_score', 'ex2_phonol_score',
            'ex3_criterion1_score', 'ex3_criterion2_score',
            'total_score'],
        'header_rows': 2,
    },
    'A2': {
        'column_names': ['exam_origname', 'exam_id', 'evaluator_id',
           'ex1_selfdescr_score', 'ex1_eventdescr_score', 'ex1_lexgram_score',
           'ex2_imgdescr_score', 'ex2_response_score', 'ex2_lexgram_score',
           'ex3_questions_score', 'ex3_lexgram_score',
           'total_interact_score', 'total_cohesion_score', 'total_phonol_score', 'total_score'],
        'header_rows': 3,
    },
    'A2_older': {
        'column_names': ['exam_id', 'evaluator_id',
                 'ex1_response', 'ex1_lexical', 'ex1_grammar',
                 'ex2_response', 'ex2_questions', 'ex2_lexical', 'ex2_grammar',
                 'total_phoninter', 'total_score', 'total_percentage'],
        'header_rows': 1,
    },
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

    # recast all "_score" columns to Int64 to allow for null values
    score_column = data.columns[data.columns.str.endswith('_score')]
    data[score_column] = data[score_column].astype('Int64')

    # extract the first row which contains the maximum scores and remove it from the data
    max_scores = data.iloc[0]
    #print(f'Maximum scores: {max_scores}')
    data.drop(index=0, inplace=True)

    # add new columns with percentage values calculated from the scores normalized to the maximum scores
    for key in data.columns:
        if not key.endswith('_score'):
            continue
        # calculate the percentage value
        new_key = key.replace('_score', '_perc')
        data[new_key] = data[key] / int(max_scores[key])

        # locate the values of the new column that are not in the range [0, 1] and warn the user
        if not data[new_key].between(0, 1).all():
            print(f'Warning: the values of the column {new_key} are not in the range [0, 1]')
            # print the values that are not in the range [0, 1]
            print(data.loc[~data[new_key].between(0, 1), ['exam_id', 'evaluator_id', new_key]])

def get_json_filename(exam_id, audio_dir, output_dir):
    for f in os.listdir(audio_dir):
        # Skip files that don't start with the exam_id
        if not f.startswith(exam_id):
            continue
        # Replace the .mp3 extension with .json
        filename = f.replace('.mp3', '.json')
        yield f'{output_dir}/{filename}'

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('labels_csv', type=str, help='The path to the CSV file containing the labels for the old exams')
parser.add_argument('output_dir', type=str, help='The directory to output the JSON files to')
parser.add_argument('--audio-dir', type=str, help='The directory containing the audio files')
parser.add_argument('--exam-type', type=str, default='A2_older', help='The type of exam to prepare the labels for')
args = parser.parse_args()


if args.exam_type not in CONFIG:
    print(f'Invalid exam type: {args.exam_type}')
    exit(1)

# Load the data from the CSV file
data = pandas.read_csv(
    args.labels_csv,
    sep="\t",
    names=CONFIG[args.exam_type]['column_names'],
    skiprows=CONFIG[args.exam_type]['header_rows'],
    index_col=False
)

#print(data)

process_data(data, args.exam_type)

# Group data by exam_id
grouped_data = data.groupby('exam_id')

# Output each row to a separate JSON file in the output directory
for exam_id, group in grouped_data:
    # create a list of evaluations for each evaluator but do not include the exam_id
    evaluations = [row.drop(['exam_id']).to_dict() for _, row in group.iterrows()]
    #print(evaluations)
    # Create the average evaluation dictionary by averaging the scores across all evaluations
    avg_evaluation = {}
    for key in group.columns:
        if key in ['evaluator_id', 'exam_id']:
            continue
        avg_evaluation[key] = group[key].mean()
    # Create the output dictionary
    out_dict = {
        'exam_id': exam_id,
        'evaluations': evaluations,
        'avg': avg_evaluation,
    }
    for output_file in get_json_filename(exam_id, args.audio_dir, args.output_dir):
        with open(output_file, 'w') as f:
            json.dump(out_dict, f, indent=4)