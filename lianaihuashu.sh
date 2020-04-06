#! /bin/bash
cd /home/ubuntu/data
name1="lianaihuashu.py"
pid1=`ps -ef | grep $name1 | grep -v grep | awk -F ' ' '{print $2}'`
if [ "$pid1"x = ""x ]; then
    echo "$name1 is off"
else
    sudo kill -9 $pid1
fi
name2="shuju.py"
pid2=`ps -ef | grep $name2 | grep -v grep | awk -F ' ' '{print $2}'`
if [ "$pid2"x = ""x ]; then
    echo "$name2 is off"
else
    sudo kill -9 $pid2
fi
name3="dingshi.py"
pid3=`ps -ef | grep $name3 | grep -v grep | awk -F ' ' '{print $2}'`
if [ "$pid3"x = ""x ]; then
    echo "$name3 is off"
else
    sudo kill -9 $pid3
fi
port0=13888
pid0=$(sudo netstat -nlp | grep :$port0 | awk '{print $7}' | awk -F"/" '{ print $1 }')
if [  -n  "$pid0"  ];  then
    sudo kill  -9  $pid0
fi
port1=18888
pid1=$(sudo netstat -nlp | grep :$port1 | awk '{print $7}' | awk -F"/" '{ print $1 }')
if [  -n  "$pid1"  ];  then
    sudo kill  -9  $pid1
fi
cd /home/ubuntu/data/lianaihuashu
nohup python lianaihuashu.py > /home/ubuntu/data/lianaihuashu/lianaihuashu.txt 2>&1 &
cd /home/ubuntu/data/lianaihuashu
nohup python shuju.py > /home/ubuntu/data/lianaihuashu/shuju.txt 2>&1 &
cd /home/ubuntu/data/lianaihuashu
nohup python dingshi.py > /home/ubuntu/data/lianaihuashu/dingshi.txt 2>&1 &
