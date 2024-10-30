#!/bin/bash

cwd=$(pwd)
pushd ../../

for shuf in 1.0 1.5 2.5 5.0 10.0
do
    shuf_two_decimals=$(echo $shuf | awk '{printf "%04.1f", $1}')
    python combiner.py --input_files runs/data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_${shuf}+lr_1e-5+accumulation_steps_4+r_drop_1*+dropout_0.1+fold_*/predictions.json --attribute HAS_RESIDENCE-predicted > $cwd/res_HR_${shuf_two_decimals}.txt
done
shuf_two_decimals=20.0
python combiner.py --input_files runs/data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+lr_1e-5+accumulation_steps_4+r_drop_1*+dropout_0.1+fold_*/predictions.json --attribute HAS_RESIDENCE-predicted > $cwd/res_HR_${shuf_two_decimals}.txt

popd
grep macro res_HR_* | sed 's/ \+/ /g' | cut -f6 -d' '