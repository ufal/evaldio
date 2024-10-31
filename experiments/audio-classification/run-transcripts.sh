#!/bin/bash

#SBATCH -p gpu-ms,gpu-troja
#SBATCH -G 1
#SBATCH -C "gpuram24G|gpuram40G|gpuram48G|gpuram95G"
#SBATCH --mem=20G
#SBATCH --cpus-per-task=4

lr=$1
batch_size=$2
rdrop=$3
dropout=$4

ex_name="transcripts+deleted+sr_16000+dur_20.0+min_dur_10.0+ex_False+lr_${lr}+batch_size_${batch_size}_r_drop_${rdrop}_dropout_${dropout}"

srun python run-transcripts.py \
    --train_folds ../datalists/fold_0.20241008.tsv \
    ../datalists/fold_1.20241008.tsv \
    ../datalists/fold_2.20241008.tsv \
    ../datalists/fold_3.20241008.tsv \
    ../datalists/fold_4.20241008.tsv \
    ../datalists/fold_5.20241008.tsv \
    ../datalists/fold_6.20241008.tsv \
    ../datalists/fold_7.20241008.tsv \
    --dev_folds ../datalists/fold_9.20241008.tsv \
    --test_folds ../datalists/fold_9.20241008.tsv \
    --h5_file data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+mikr-whisper-large-v3-czech-cv13.h5 \
    --batch_size $batch_size \
    --lr $lr \
    --max_epochs 10 \
    --r_drop $rdrop \
    --experiment_name $ex_name \
    --dropout $dropout 