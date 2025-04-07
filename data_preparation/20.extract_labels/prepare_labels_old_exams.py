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
    'B1': {
        'column_names': ['exam_origname', 'exam_id', 'evaluator_id',
           'ex1_imgdescr_score', 'ex1_response_score', 'ex1_lexical_score', 'ex1_grammar_score',
           'ex2_narrat_score', 'ex2_response_score', 'ex2_lexical_score', 'ex2_grammar_score',
           'ex3_commgoal_score', 'ex3_interact_score', 'ex3_lexical_score', 'ex3_grammar_score',
           'total_phonol_score', 'total_score'],
        'header_rows': 2,
    },
}

OVERALL_CONFIG = {
    'column_idx' : [0, 4, 5, 14],
    'column_names': ['exam_split_id', 'level', 'etalon_perc', 'etalon_score'],
}

def process_overall_data(data, level):
    # Extract the relevant columns
    data = data.iloc[:, OVERALL_CONFIG['column_idx']]
    # Rename the columns
    data.columns = OVERALL_CONFIG['column_names']
    # Discard all the rows that do not match the selected level
    data = data[data['level'] == level]
    # Add the exam_id column which is derived from the exam_split_id column and drop the exam_split_id column
    data['exam_id'] = data['exam_split_id'].astype(str).apply(lambda x: "_".join(x.split("_")[0:3]))
    data.drop(columns=['exam_split_id'], inplace=True)
    # Group the data by exam_id, keeping just the first row
    # Warn if there are multiple rows for the same exam_id
    # Set the 'exam_id' row to be the index of the new table
    grouped_data = data.groupby('exam_id')
    #duplicates = grouped_data.filter(lambda x: len(x) > 1)
    #print(f'Warning: there are {len(duplicates)} duplicates in the overall data')
    #print(duplicates)
    data = grouped_data.first()
    return data

def process_detailed_data(data, exam_type):
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
parser.add_argument('--overall-csv', type=str, help='The path to the CSV file containing the overall scores')
args = parser.parse_args()

if args.exam_type not in CONFIG:
    print(f'Invalid exam type: {args.exam_type}')
    exit(1)

overall_dict = {}
if args.overall_csv:
    # Load the data from the CSV file
    overall_data = pandas.read_csv(
        args.overall_csv,
        sep="\t",
        index_col=False
    )
    overall_data = process_overall_data(overall_data, args.exam_type)
    overall_dict = overall_data.to_dict(orient='index')

# Load the data from the CSV file
detailed_data = pandas.read_csv(
    args.labels_csv,
    sep="\t",
    names=CONFIG[args.exam_type]['column_names'],
    skiprows=CONFIG[args.exam_type]['header_rows'],
    index_col=False
)
#print(data)
process_detailed_data(detailed_data, args.exam_type)

# Try to output each row in the overall data associated with the selected level as a separate JSON file
for exam_id, group in detailed_data.groupby('exam_id'):
    # create a list of evaluations for each evaluator but do not include the exam_id
    evaluations = [row.drop(['exam_id']).to_dict() for _, row in group.iterrows()]
    #print(evaluations)
    # Create the average evaluation dictionary by averaging the scores across all evaluations
    avg_evaluation = {}
    for key in group.columns:
        if key in ['evaluator_id', 'exam_id']:
            continue
        avg_evaluation[key] = group[key].mean()
    # Add the etalon scores and percs to the average evaluation dictionary if available
    if exam_id in overall_dict:
        avg_evaluation['etalon_perc'] = overall_dict[exam_id]['etalon_perc']
        avg_evaluation['etalon_score'] = overall_dict[exam_id]['etalon_score']
        # delete the record indexed by exam_id from the overall_dict
        del overall_dict[exam_id]
    # Create the output dictionary
    out_dict = {
        'exam_id': exam_id,
        'evaluations': evaluations,
        'avg': avg_evaluation,
    }
    # Output the labels to the JSON file
    # The filename of the JSON file is determined by the files in the audio_dir
    # If there are multiple files of the same exam (different parts), the same JSON file is used for all of them
    # This also ensures that the JSON file is created only if the audio file exists
    for output_file in get_json_filename(exam_id, args.audio_dir, args.output_dir):
        with open(output_file, 'w') as f:
            json.dump(out_dict, f, indent=4)

# Process any exam_ids in the overall_dict that are not in the detailed data
for exam_id in overall_dict:
    avg_evaluation = {}
    avg_evaluation['etalon_perc'] = overall_dict[exam_id]['etalon_perc']
    avg_evaluation['etalon_score'] = overall_dict[exam_id]['etalon_score']
    # Create the output dictionary
    out_dict = {
        'exam_id': exam_id,
        'evaluations': [],
        'avg': avg_evaluation,
    }
    # Output the labels to the JSON file
    # The filename of the JSON file is determined by the files in the audio_dir
    # If there are multiple files of the same exam (different parts), the same JSON file is used for all of them
    # This also ensures that the JSON file is created only if the audio file exists
    for output_file in get_json_filename(exam_id, args.audio_dir, args.output_dir):
        with open(output_file, 'w') as f:
            json.dump(out_dict, f, indent=4)