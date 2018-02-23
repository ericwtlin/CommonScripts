#!/bin/sh
PROCESS_FLAG="preprocess.py"
MAX_PROCESS_NUM=3

index_begin=0
index_end=5

###########AUTOMATION######################

index=$index_begin
while :
do
sleep 180	#detect every 180 seconds
count=`ps -ef |grep $PROCESS_FLAG |grep -v "grep" |wc -l`
if [ $count -lt $MAX_PROCESS_NUM ]
then
    nohup python preprocess.py corpus_${index}.0.txt pair/pair_${index}.txt &
    index=`expr $index + 1`
fi

if [ $index -gt $index_end ]
then
    echo "All the commands have been started"
    break
fi

echo "Current working process num:${count}" 
done
