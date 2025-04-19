#!/bin/bash

#SBATCH -p gpu-ms,gpu-troja
#SBATCH -G 1
#SBATCH -C "gpuram40G|gpuram48G|gpuram95G"
#SBATCH --mem=40G
#SBATCH --cpus-per-task=4
#SBATCH --exclude=dll-4gpu3

lr=$1
accumulation_steps=$2
batch_size=$3
dropout=$4
fold=$5
h5_file=$6
max_epochs=$7
train_last_layer=$8
if [ "$train_last_layer" = "true" ]; then
    train_last_layer="--train_last_layer"
    train_last_layer_str="+train_last_layer_true"
else
    train_last_layer=""
fi
r_drop=$9

ex_name="+dataset_${h5_file##*/}+folds_10+fold_${fold}+lr_${lr}+batch_size_${batch_size}+accumulation_steps_${accumulation_steps}+dropout_${dropout}+max_epochs_${max_epochs}${train_last_layer_str}+rdrop_${r_drop}"

ex_folder="runs/${ex_name}/version_*/checkpoints/last.ckpt"
ls $ex_folder
predict=''
if ls ${ex_folder} 1> /dev/null 2>&1; then
    echo "Training already completed for ${ex_name}. Predicting..."
    ckpt=$(ls $ex_folder | head -n 1)
    predict="--ckpt_path $ckpt"
fi

srun python run.py \
    --num_folds 10 \
    --dev_fold $fold \
    --test_fold $fold \
    --h5_file $h5_file \
    --batch_size $batch_size \
    --accumulation_steps $accumulation_steps \
    --lr $lr \
    --max_epochs $max_epochs \
    --experiment_name $ex_name \
    --dropout $dropout \
    --r_drop $r_drop \
    $predict $train_last_layer