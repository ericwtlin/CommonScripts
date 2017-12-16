#!/bin/sh
while :
do
sleep 180	#detect every 180 seconds
count=`ps -ef |grep "sh exec.sh" |grep -v "grep" |wc -l`
#echo $count
if [ $count -eq 0 ]
then
	echo "work have end"
	sh /home/eric-lin/crf-workspace/exec-2.sh
	break
else
	echo "still working"
fi
done
