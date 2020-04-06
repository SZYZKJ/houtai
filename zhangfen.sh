#! /bin/bash
cd /home/ubuntu/data
name1="zhangfen.py"
pid1=`ps -ef | grep $name1 | grep -v grep | awk -F ' ' '{print $2}'`
if [ "$pid1"x = ""x ]; then
    echo "$name1 is off"
else
    sudo kill -9 $pid1
fi
port0=14888
pid0=$(sudo netstat -nlp | grep :$port0 | awk '{print $7}' | awk -F"/" '{ print $1 }')
if [  -n  "$pid0"  ];  then
    sudo kill  -9  $pid0
fi
cd /home/ubuntu/data/lianaihuashu
nohup python zhangfen.py > /home/ubuntu/data/lianaihuashu/zhangfen.txt 2>&1 &
