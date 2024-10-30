#!/bin/bash

#SBATCH -p gpu-ms,gpu-troja
#SBATCH -G 1
#SBATCH -C "gpuram24G|gpuram40G|gpuram95G"
#SBATCH --mem=20G
#SBATCH --cpus-per-task=4

python transcribe.py \
    --datalist ../datalists/all.20241008.resident_labels.tsv \
    --h5_file data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True.h5 \
    --batch_size 8 --num_beams 1 --model_id 'mikr/whisper-large-v3-czech-cv13'