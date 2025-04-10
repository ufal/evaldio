        # "ex1_response": 3,
        # "ex1_lexical": 2,
        # "ex1_grammar": 2,
        # "ex2_response": 2,
        # "ex2_questions": 3,
        # "ex2_lexical": 2,
        # "ex2_grammar": 3,
        # "ex12_phoninter": 3,
        # "result": true,
results=results/20_folds_rdrop300
mkdir -p ${results}

for attr in result "ex1_response" "ex1_lexical" "ex1_grammar" "ex2_response" "ex2_questions" "ex2_lexical" "ex2_grammar" "ex12_phoninter"
do
    python combiner.py --input_files runs/*rdrop_300*/predictions.json --attribute ${attr}-predicted --confusion_matrix ${results}/${attr}-confusion-matrix.png 2>&1 > ${results}/${attr}-confusion-matrix.log
done