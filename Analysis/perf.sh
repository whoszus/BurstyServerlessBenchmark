########################################################################## 
# File Name: perf_collect.sh 
# Author: Chengzhi Lu 
# mail: cz.lu@siat.ac.cn 
# Created Time: Fri Aug 6 06:54:10 2021 
######################################################################### 
#!/bin/zsh 
# 用 来 采 集 perf的 相 关 指 标 ,默 认 使 用 perf stat 
# 使 用 方 法 ： bash perf_collect.sh -e "perf_event" -I "Interval of record" 
event=${1:-'LLC-load-misses'} 
interval=${2:-'500'}
namespace=${3:-'default'}
kubectl get node -o wide|grep -v "NAME"|awk '{print $1,$6}'> node.t
TIMESTAMP=`date +%s.%N`
cat node.t | while read n
do
    echo 'handling -----------'$n
    node_name=$(echo $n|awk '{print $1}')
    ip=$(echo $n|awk '{print $2}')
    ssh -n $ip 'cd /home/tmp/ && rm *.csv ' 2>&1&    
    for pod in $(kubectl get pod -o wide -n $namespace|grep $node_name|awk '{print $1}') 
    do 
        echo 'pod' $pod ' in node' $node_name 2>&1& 
        pid=$(ssh -n $ip 'cat| bash /dev/stdin '$pod '< pod_pid_info.sh') 
        pid=$(echo $pid|tr -cd "[0-9]" 2>&1& ) 
        ssh -n $ip perf stat -e $event -I $interval -p $pid -o "/home/tmp/"$node_name'_'$pod'_'$TIMESTAMP".csv" 2>&1& 
    done
done
# sleep 5
# for n in $(kubectl get node -o wide|grep -v "NAME"|awk '{print $6}') 
# do
#     scp -r 172.169.8.193:/home/tmp/ 
# done 