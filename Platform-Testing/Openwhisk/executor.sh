#!/bin/bash
PRINTLOG=false
ACTIONNAME=''
TIMES=''
PARAMS=''
while getopts "a:t:p:lWR" OPT; do
    case $OPT in
    a)
      ACTIONNAME=$OPTARG
      LOGFILE=$ACTIONNAME.csv
      ;;
    t)
      TIMES=$OPTARG
      ;;

    # "Warm up only" with this argument: warm up and then exit with no output.
    p)
      
      PARAMS=$(echo $OPTARG | sed $'s/\'//g')
        ;;
    ?)
        echo "unknown arguments"
    esac
done

if [[ -z $TIMES ]];then
  TIMES=1
fi


if [[ $PRINTLOG = true && ! -e $LOGFILE ]]; then
    echo logfile:$LOGFILE
    echo "invokeTime,startTime,endTime" > $LOGFILE
fi

LATENCYSUM=0
for i in $(seq 1 $TIMES)
do

    echo Measure start up time: no.$i
    invokeTime=`date +%s%3N`
    times=`wsk -i action invoke $ACTIONNAME --blocking --result $PARAMS` 
    endTime=`date +%s%3N`
    startTime=`echo $times | jq -r '.startTime'`
    echo "{'invokeTime': $invokeTime, 'startTime': $startTime, 'endTime': $endTime}"
    
    # latency=`expr $endTime - $invokeTime`
    # LATENCYSUM=`expr $latency + $LATENCYSUM`
    # # The array starts from array[1], not array[0]!
    # LATENCIES[$i]=$latency

    # if [[ $PRINTLOG = true ]];then
    #     echo "$invokeTime,$startTime,$endTime" >> $LOGFILE
    # fi
done

# Sort the latencies
# for((i=0; i<$TIMES+1; i++)){
#   for((j=i+1; j<$TIMES+1; j++)){
#     if [[ ${LATENCIES[i]} -gt ${LATENCIES[j]} ]];then
#       temp=${LATENCIES[i]}
#       LATENCIES[i]=${LATENCIES[j]}
#       LATENCIES[j]=$temp
#     fi
#   }
# }

# echo "------------------ result ---------------------"
# _50platency=${LATENCIES[`echo "$TIMES * 0.5"| bc | awk '{print int($0)}'`]}
# _75platency=${LATENCIES[`echo "$TIMES * 0.75"| bc | awk '{print int($0)}'`]}
# _90platency=${LATENCIES[`echo "$TIMES * 0.90"| bc | awk '{print int($0)}'`]}
# _95platency=${LATENCIES[`echo "$TIMES * 0.95"| bc | awk '{print int($0)}'`]}
# _99platency=${LATENCIES[`echo "$TIMES * 0.99"| bc | awk '{print int($0)}'`]}

# echo "Latency (ms):"
# echo -e "Avg\t50%\t75%\t90%\t95%\t99%\t"
# echo -e "`expr $LATENCYSUM / $TIMES`\t$_50platency\t$_75platency\t$_90platency\t$_95platency\t$_99platency\t"

# if [ ! -z $RESULT ]; then
#     echo -e "\n\n------------------ (single)result ---------------------\n" >> $RESULT
#     echo "mode: $MODE, loop_times: $TIMES, warmup_times: $WARMUP" >> $RESULT
#     _50platency=${LATENCIES[`echo "$TIMES * 0.5"| bc | awk '{print int($0)}'`]} 
#     _75platency=${LATENCIES[`echo "$TIMES * 0.75"| bc | awk '{print int($0)}'`]} 
#     _90platency=${LATENCIES[`echo "$TIMES * 0.90"| bc | awk '{print int($0)}'`]} 
#     _95platency=${LATENCIES[`echo "$TIMES * 0.95"| bc | awk '{print int($0)}'`]} 
#     _99platency=${LATENCIES[`echo "$TIMES * 0.99"| bc | awk '{print int($0)}'`]}

#     echo "Latency (ms):" >> $RESULT
#     echo -e "Avg\t50%\t75%\t90%\t95%\t99%\t" >> $RESULT
#     echo -e "`expr $LATENCYSUM / $TIMES`\t$_50platency\t$_75platency\t$_90platency\t$_95platency\t$_99platency\t" >> $RESULT
# fi