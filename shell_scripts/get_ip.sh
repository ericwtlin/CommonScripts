#!/usr/bin/env bash

# get ips of www.qichacha.com

ips=`dig +noall +answer www.qichacha.com | awk '$4=="A"{print $5}'`
#ips=`getent hosts www.qichacha.com|awk '{print $1}'`
for ip in $ips;
do
    echo ${ip}

done

exit