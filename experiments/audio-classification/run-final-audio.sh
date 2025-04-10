

# lr=$1
# accumulation_steps=$2
# batch_size=$3
# dropout=$4
# fold=$5
# h5_file=$6
# max_epochs=$7
# export CUDA_VISIBLE_DEVICES=3
for h5_file in "data/sr_16000+dur_20.0+min_5.0+exam_False.h5"
do
    for fold in 0 1 2 3 4 5 6 7 8 9 
    do
        for lr in 1e-05
        do
            for accumulation_steps in 4
            do
                for batch_size in 4
                do
                    for dropout in 0.1
                    do
                        for max_epochs in 6
                        do
                            for r_drop in 300 #0.1 0.3 0.5
                            do
                                sbatch run.sh $lr $accumulation_steps $batch_size $dropout $fold $h5_file $max_epochs false $r_drop
                            done
                        done
                    done
                done
            done
        done
    done
done
