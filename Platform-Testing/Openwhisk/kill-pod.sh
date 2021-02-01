for p in $( kubectl get pods -n ow | grep  guest | tail -n +2 | awk -F ' ' '{print $1}'); do kubectl delete pod -n ow $p --grace-period=0 --force;done
