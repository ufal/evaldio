
# for h5_file in "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True" \
#                "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_2.5" \
#                 "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_5.0" \
#                 "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_10.0" \
#                 "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_1.5" \
#                 "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_1.0" 
# do
#     for fold in 0 1 2 3 4 5 6 7 8 9
#     do
#         for lr in 1e-5
#         do
#             for accumulation_steps in 4
#             do
#                 for rdrop in 0.0
#                 do
#                     for dropout in 0.1
#                     do
#                         sbatch run.sh $lr $accumulation_steps $rdrop $dropout $fold $h5_file 6
#                     done
#                 done
#             done
#         done
#     done
# done



for h5_file in  "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_2.5" 
    #"data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True" \
            #    "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_2.5" \
            #     "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_5.0" \
            #     "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_10.0" \
            #     "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_1.5" \
            #     "data/v_deleted+sr_16000+dur_20.0+min_dur_10.0+ex_True+shuf_1.0" 
do
    for fold in 0 1 2 3 4 5 6 7 8 9
    do
        for lr in 1e-5
        do
            for accumulation_steps in 4
            do
                for rdrop in 0.0
                do
                    for dropout in 0.1
                    do
                        sbatch run.sh $lr $accumulation_steps $rdrop $dropout $fold $h5_file 6 "--examiner_only"
                    done
                done
            done
        done
    done
done