event=${1:-'LLC-load-misses'} 
interval=${2:-'500'}
namespace=${3:-'openfaas-fn'}
kubectl get node -o wide|grep -v "NAME"|awk '{print $1,$6}'> node.t
TIMESTAMP=`date +%s.%N`
cat node.t | while read n
do
    echo 'handling -----------'$n
    node_name=$(echo $n|awk '{print $1}')
    ip=$(echo $n|awk '{print $2}')
    ssh -n $ip 'cd /home/tmp/ && rm *.csv ' 2>&1& 
    echo $ip'....'$node_name'..........'$event  
    for pod in $(kubectl get pod -o wide -n $namespace|grep $node_name|awk '{print $1}') 
    do 
        echo 'pod' $pod ' in node' $node_name 2>&1& 
        cmd='curl http://172.169.8.254:10000/files/awsometools/shell/node_pid.sh |bash -s '$pod
        pidstring=$(ssh -n $ip $cmd)
        pid=$(echo $pidstring|tr -cd "[0-9]" 2>&1& )
        echo 'pid----------'$pid
        ssh -n $ip perf stat -e $event -I $interval -p $pid -o "/home/tmp/"$node_name'_'$pod'_'$TIMESTAMP".csv" 2>&1& 
    done
done