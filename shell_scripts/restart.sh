#!/bin/bash

cd `dirname $0`

count=`ps -ef |grep "shadowsocks/local.py" |grep -v "grep" |wc -l`
if [ $count -gt 0 ]
then
    # automatically kill the existing local.py
    for pid in $(ps -ef | grep "shadowsocks/local.py" | grep -v "grep" | awk '{print $2}'); do
	echo "Kill $pid"
        sudo kill $pid
    done
    echo "The existing local.py has been killed. Restart now."
fi


if [ $# -eq 0 ]
then
    nohup python ./shadowsocksR/shadowsocks/local.py -c ./config.json >/dev/null 2>&1 &
else
    nohup python ./shadowsocksR/shadowsocks/local.py -c $1 >/dev/null 2>&1 &
fi

count=`ps -ef |grep "shadowsocks/local.py" |grep -v "grep" |wc -l`
if [ $count -eq 1 ]
then
    echo "ShadowsocksR started."
fi