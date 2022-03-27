########################################################################## 
# File Name: pod_pid_info.sh 
# Author: chengzhilu 
# mail: czlu@siat.ac.cn 
# Created Time: Fri Aug 6 14:33:56 2021 
######################################################################### 
#!/usr/bin/env bash 
Check_jq() { 
which jq &> /dev/null 
if [ $? != 0 ];then 
echo "no jq" 
`apt-get install -y jq 2>/dev/null` 
exit 1 
fi 
} 
Pid_info() { 
docker_storage_location=`docker info | grep 'Docker Root Dir' | awk '{print $NF}'` 
for docker_short_id in `docker ps | grep ${pod_name} | grep -v pause | awk '{print $1}'` 
do 
docker_long_id=`docker inspect ${docker_short_id} | jq ".[0].Id" | tr -d '"'` 
cat ${docker_storage_location}/containers/${docker_long_id}/config.v2.json | jq ".State.Pid" 
done 
} 
pod_name=$1 
# Check_jq 
Pid_info 