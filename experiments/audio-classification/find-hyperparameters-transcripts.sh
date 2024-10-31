for lr in 1e-5 1e-6 1e-7
do
    for batch_size in 4 8 16 32
    do
        for rdrop in 0.
        do
            for dropout in 0.1
            do
                sbatch run-transcripts.sh $lr $batch_size $rdrop $dropout
            done
        done
    done
done