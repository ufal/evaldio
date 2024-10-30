#!/bin/bash

#SBATCH -p gpu-ms,gpu-troja
#SBATCH -G 1
#SBATCH -C "gpuram40G|gpuram48G|gpuram95G"
#SBATCH --mem=40G
#SBATCH --cpus-per-task=4
#SBATCH --exclude=dll-4gpu3

lr=$1
accumulation_steps=$2
rdrop=$3
dropout=$4
fold=$5
h5_file=$6
max_epochs=$7

ex_name="${h5_file}+lr_${lr}+accumulation_steps_${accumulation_steps}+r_drop_${rdrop}+dropout_${dropout}+fold_${fold}"

ex_folder="runs/${ex_name}/version_*/checkpoints/last.ckpt"
ls $ex_folder
if ls ${ex_folder} 1> /dev/null 2>&1; then
    echo "Training already completed for ${ex_name}. Skipping..."
    exit 0
fi

srun python run.py \
    --train_folds ../datalists/fold_0.20241008.tsv \
    ../datalists/fold_1.20241008.tsv \
    ../datalists/fold_2.20241008.tsv \
    ../datalists/fold_3.20241008.tsv \
    ../datalists/fold_4.20241008.tsv \
    ../datalists/fold_5.20241008.tsv \
    ../datalists/fold_6.20241008.tsv \
    ../datalists/fold_7.20241008.tsv \
    ../datalists/fold_8.20241008.tsv \
    ../datalists/fold_9.20241008.tsv \
    --dev_folds ../datalists/fold_${fold}.20241008.tsv \
    --test_folds ../datalists/fold_${fold}.20241008.tsv \
    --h5_file ${h5_file}.h5 \
    --batch_size 4 \
    --accumulation_steps $accumulation_steps \
    --lr $lr \
    --max_epochs $max_epochs \
    --r_drop $rdrop \
    --experiment_name $ex_name \
    --dropout $dropout 