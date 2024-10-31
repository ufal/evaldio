for lr in 1e-5
do
    for accumulation_steps in 1
    do
        for rdrop in 1. 3. 5.
        do
            for dropout in 0.1 0.2 0.3
            do
                sbatch run.sh $lr $accumulation_steps $rdrop $dropout
            done
        done
    done
done