#!/bin/bash
PRINTLOG=false
ACTIONNAME=''
TIMES=''
PARAMS=''
PLATFORM=''
UUID=''
while getopts "a:t:p:P:u:lWR" OPT; do
    case $OPT in
    a)
      ACTIONNAME=$OPTARG
      ;;
    t)
      TIMES=$OPTARG
      ;;

    # "Warm up only" with this argument: warm up and then exit with no output.
    p)
      
      PARAMS=$(echo $OPTARG | sed $'s/\'//g')
        ;;
    P)  
        PLATFORM=$OPTARG
        ;;
    u)
        UUID=$OPTARG
        ;;
    ?)
        echo "unknown arguments"
    esac
done

if [[ -z $TIMES ]];then
  TIMES=1
fi


LATENCYSUM=0
for i in $(seq 1 $TIMES)
do
    invokeTime=`date +%s.%N`
    times=`wsk -i action invoke $ACTIONNAME --blocking --result`
    endTime=`date +%s.%N`
    startTime=`echo $times | jq -r '.startTime'`
    if [ ! $startTime ]; then  
        startTime="''"
    fi
    echo "$UUID,$PLATFORM,$ACTIONNAME,$invokeTime,$startTime,$endTime" >> result_$PLATFORM.csv
done
