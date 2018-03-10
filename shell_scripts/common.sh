#!/usr/bin/env bash


echo "change the working directory to the parent dir of this shell script, but not where we activate the script"
echo '$0: '$0
echo `dirname $0`
echo "pwd: "`pwd`
echo "============================="
echo "scriptPath1: "$(cd `dirname $0`; pwd)     #right
echo "scriptPath2: "$(pwd)                      #wrong
echo "scriptPath3: "$(dirname $(readlink -f $0))    #right
echo "scriptPath4: "$(cd $(dirname ${BASH_SOURCE:-$0});pwd)     #right
echo -n "scriptPath5: " && dirname $(readlink -f ${BASH_SOURCE[0]})     #right
#thus, to change the working directory to the parent dir of this shell script:
cd `dirname $0`


# printing time
echo "`date +%c` hello world"
echo `date +%c` "hello world"
