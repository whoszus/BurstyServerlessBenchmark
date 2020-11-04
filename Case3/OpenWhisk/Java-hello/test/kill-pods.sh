for p in $( kubectl get pods -n openwhis | grep  hello | tail -n +2 | awk -F ' ' '{print $1}'); do kubectl delete pod -n openwhis $p --grace-period=0 --force;done
