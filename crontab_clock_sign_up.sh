#!/bin/bash -x

export PATH=/usr/local/bin:/usr/bin:/sbin:/bin

home=$(cd $(dirname $0);pwd)
cd $home

ts=`date +%Y%m`

for file in 1.py; do
	if [ $# -eq 1 ]; then
		ps -ef | grep "$home/$file" | grep -v "grep" | awk '{print $2}' | while read pid; do kill -9 $pid; done
		sleep 1
	fi

	cnt=$(ps -ef | grep  "$home/$file" | grep -v "grep"| wc -l)
	if [ $cnt -eq 0 ];then
		/usr/bin/python $home/$file clock_sign_up >> ./log/${file}.${ts}.log 2>&1 &
	fi
done