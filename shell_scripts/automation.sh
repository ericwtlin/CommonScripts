#!/usr/bin/env bash

DEBUG="False"
#FORCE="False"
#DEBUG="True"
FORCE="True"

Ks=($1)  #10% of origin training set
tag_top_ratio=$2

if [ $# -ge 3 ]; then
MAX_ITER_NUM=$3
else
MAX_ITER_NUM=15
fi

if [ $DEBUG == "True" ]
then
    FORCE="True"
    epoch_num=2
    MAX_ITER_NUM=3
    Ks=(270)
fi

for ((i=0;i<${#Ks[@]};i++));
    do
    K=${Ks[i]}

    mkdir ${save_dir_base}

    cur_iter=$START_ITER

    convengent=2    #1: convergent; 2: not convergent yet
    while [ $convengent -ne 1 -a $cur_iter -le $MAX_ITER_NUM ]; do
        save_dir="${data_set_name}/with_pseudo_${K}_tag_top_ratio${tag_top_ratio}/iter${cur_iter}"

        if [ $cur_iter -eq 0 ]; then
            echo "`date +%c` Iter: ${cur_iter}, Copy the fine-tuned model (by supervised corpus)."
            echo "`date +%c` Iter: ${cur_iter}, Copy the fine-tuned model (by supervised corpus)." >> ${whole_log_path}
        else
            echo "`date +%c` Iter: ${cur_iter}, To predict pseudo labels, selected top ${K} & tag_top_ratio=${tag_top_ratio} to save in ${cur_pseudo_corpus_selected_txt_absolute_path}, the rest saved in ${cur_pseudo_corpus_unselected_txt_absolute_path}"
            echo "`date +%c` Iter: ${cur_iter}, To predict pseudo labels, selected top ${K} & tag_top_ratio=${tag_top_ratio} to save in ${cur_pseudo_corpus_selected_txt_absolute_path}, the rest saved in ${cur_pseudo_corpus_unselected_txt_absolute_path}" >> ${whole_log_path}

            #fi
        fi

        python compare_pseudo_corpus.py ${former_validation_result_fullpath} ${cur_validation_result_fullpath} ${save_dir_base}/${save_dir}/compare_pseudo_corpus.log
        convengent=$?

        cur_iter=`expr $cur_iter + 1`
    done

    echo "K=$K done!"
done

exit
