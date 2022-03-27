cat node.t |while read n
do 
    node_name=$(echo $n|awk '{print $1}')
    ip=$(echo $n|awk '{print $2}')

    for node in $ip
    do
        ssh $ip 'pkill perf'
        ssh $ip tar -zcP --file=/home/$node_name.tar.gz /home/tmp/
        scp $ip:/home/$node_name.tar.gz ./perf
    done 
done