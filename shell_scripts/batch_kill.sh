#!/bin/bash

cd `dirname $0`
PROCESS_FLAG="preprocess_new.py"

count=`ps -ef |grep ${PROCESS_FLAG} |grep -v "grep" |wc -l`
if [ $count -gt 0 ]
then
    # automatically kill the existing processes
    for pid in $(ps -ef | grep ${PROCESS_FLAG} | grep -v "grep" | awk '{print $2}'); do
    echo "Kill $pid"
        kill $pid
    done
    echo "The existing processes have been killed."
fi
