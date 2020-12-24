nohup kubectl port-forward --namespace kubeapps svc/acoustic-adjustment-spark-master-svc 9090:80 --address 0.0.0.0 > /tmp/log.s 2> 1 &
nohup kubectl port-forward -n kubeapps svc/kubeapps --address 0.0.0.0 80:80 > /tmp/log.s 2> 1 &
nohup  kubectl port-forward -n spark mere-cars-hdfs-namenode-0 50070:50070 --address 0.0.0.0 > /tmp/log.s 2> 1 &



nohup kubectl port-forward  svc/prometheus-operator-1606189435-grafana --address 0.0.0.0 8080:80 > /tmp/log.s 2> 1 &

kubectl get secret prometheus-operator-1606189435-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo