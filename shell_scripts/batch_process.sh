#!/bin/bash
PROCESS_FLAG="preprocess.py"
MAX_PROCESS_NUM=5

index_begin=1
index_end=5

###########AUTOMATION######################

index=$index_begin
while true
do
count=`ps -ef |grep $PROCESS_FLAG |grep -v "grep" |wc -l`
if [ $count -lt $MAX_PROCESS_NUM ]
then
    run_time=0
    while $run_time == 0
    do
        if [ ! -f "data/pair/pair_${index}.txt" ]; then
            nohup python preprocess.py data/corpus_${index}.0.txt data/wvect.txt data/word2id.txt data/id2word.txt data/topfrequent.txt data/pair/pair_${index}.pkl &
            run_time = `expr $run_time + 1`
            #echo "preprocessing! $index"
        fi
        index=`expr $index + 1`
    done
fi

if [ $index -gt $index_end ]
then
    echo "All the commands have been started"
    break
fi

echo "Current working process num:${count}, the next index is: $index"
sleep 3 #detect every 180 seconds
done