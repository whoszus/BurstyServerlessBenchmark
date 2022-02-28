import os
import time
from matplotlib.pyplot import plasma
import pandas as pd
import requests
from kubernetes import client, config
from threading import Timer



class FunctionCount:
    cols = ['pod_ip', 'name', 'namespace', 'host_ip']
    count_cols = ['time', 'function_name', 'count']
    action_names = ['hello-python', 'hash-python', 'cryptography-python', 'md5-python', 'sort-python', 'facerecognition-general', 'multinomialnb-general',
                    'passiveaggressiveclassifier-general', 'perceptron-general', 'randomforestregressor-general', 'sgdclassifier-general', 'sgdregressor-general', 'svr-general', 'bigdata', 'stream']

    count_df_cols = ['time', 'platform', 'function_name', 'count']
    interval = 1

    pwd = os.path.dirname(__file__)
    def __init__(self,ns) -> None:
        if ns == 'openwhisk':
            for i in range(len(self.action_names)):
                self.action_names[i] = self.action_names[i].replace('-', '')


    def get_pod_in_platform(self, platform_name, ns):
        os.chdir(self.pwd)
        df = pd.DataFrame(columns=self.cols)
        config.load_kube_config()
        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_pod(ns)
        for i in ret.items:
            name_split = i.metadata.name.split('-')
            function_name = ''
            if i.metadata.namespace == 'openwhisk':
                function_name = name_split[-1]
                if function_name not in self.action_names:
                    continue
            else:
                if len(name_split) == 4:
                    function_name = name_split[0]+'-'+name_split[1]
                else:
                    function_name = name_split[0]
            data = {'pod_ip': i.status.pod_ip, 'name': function_name,
                    'namespace': i.metadata.namespace, 'host_ip': i.status.host_ip}
            dft = pd.DataFrame(data=data, columns=self.cols, index=[0])
            df = df.append(dft)
        count_df = df['name'].value_counts().to_frame().reset_index()
        count_df.columns = ['function_name', 'count']
        count_df['time'] = time.time()
        count_df['platform'] = platform_name
        count_df.to_csv('function_count_'+platform_name+'.csv', mode='a+', header=False)
        self.timer = Timer(self.interval, self.get_pod_in_platform, [platform_name, ns])
        self.timer.start()


class Perf:
    metrics = 'LLC-load-misses,branch-misses'
    period = 500 #ms
    ns = 'kl' # openfaas, openwhisk
    pwd = os.path.dirname(__file__)
    platform_name = 'Kubeless'


    def __init__(self,ns,metrics,platform_name) -> None:
        self.ns=ns
        self.platform_name= platform_name
        if metrics:
            self.metrics=metrics
    
    def start_perf(self):
        os.chdir(self.pwd)
        cmd = "bash perf.sh '{metrics}' {period} {ns}".format(metrics=self.metrics,period=self.period,ns= self.ns)
        os.system(cmd)        


    def stop_perf(self):
        os.chdir(self.pwd)
        cmd ='bash perf_stop_get_data.sh '+self.platform_name
        os.system(cmd)


class Prometheus:
    perf_metrics = ['node_perf_cpu_migrations_total','node_perf_branch_misses_total','node_perf_context_switches_total','node_perf_cache_bpu_read_misses_total']
    columns=['timestamp','value','cpu','metrics','node']
    system_columns=['timestamp','value','pod','metrics']
    columns_all=['timestamp','value','metrics']
    perf_columns=['time','count','unit','events']
    system_level_metrics = ['container_cpu_usage_seconds_total','container_memory_rss','container_network_receive_bytes_total']
    headers = {
        "Authorization": "Bearer eyJrIjoiVVJIZmZrUDljc1gyN0xFY1ZzRWlPZzVmYWcwNWJUTWUiLCJuIjoidGsiLCJpZCI6MX0="}
    pwd = os.path.dirname(__file__)

    def __init__(self):
        os.popen("kubectl get node -o wide|grep -v 'NAME'|awk '{print $1,$6}'> node.t>node.t")
        os.chdir(self.pwd)

    def evict_port(self,x):
        return x.split(':')[0]

    def trim_num(self,x):
        return float("{:.3f}".format(float(x)))

    def reset_time(self,x,s):
        return x-s


    def get_perf_total(self, metric_name='node_perf_cpu_migrations_total',start=1629342630,end=1629343530,step=15):
        url = 'http://serverless.siat.ac.cn:30965/api/datasources/proxy/1/api/v1/query_range?query={metric}&start={start}&end={end}&step={step}'
        metric ='sum(rate({mtr}'.format(mtr=metric_name)+ '{}[20s]))'
        url=url.format(metric=metric,start=start,end=end,step=step)
        print(url)
        r = requests.get(url,headers=self.headers)
        df = r.json()['data']['result']
        df = pd.json_normalize(df)
        dk = pd.DataFrame(columns=self.columns_all)
        for i,r in df.iterrows():
            df_values = pd.DataFrame(r['values'], columns=['timestamp','value'])
            start_time = df_values['timestamp'][0]
            df_values['metrics'] = metric_name
            df_values['timestamp']=df_values.apply(lambda x:self.reset_time(x.timestamp,start_time),axis=1)
            dk = dk.append(df_values)
        dk['value'] = dk.apply(lambda x:self.trim_num(x.value),axis=1)
        
        return dk

    def get_perf(self, metric_name='node_perf_cpu_migrations_total',start=1629342630,end=1629343530,step=15):
        url = 'http://serverless.siat.ac.cn:30965/api/datasources/proxy/1/api/v1/query_range?query={metric}&start={start}&end={end}&step={step}'
        metric ='sum(rate({mtr}'.format(mtr=metric_name)+ '{}[20s])) by (cpu,instance)'
        url=url.format(metric=metric,start=start,end=end,step=step)
        print(url)
        r = requests.get(url,headers=self.headers)
        df = r.json()['data']['result']
        df = pd.json_normalize(df)
        dk = pd.DataFrame(columns=self.columns)
        for i,r in df.iterrows():
            df_values = pd.DataFrame(r['values'], columns=['timestamp','value'])
            start_time = df_values['timestamp'][0]
            df_values['cpu'] = r['metric.cpu']
            df_values['node'] = r['metric.instance']
            df_values['metrics'] = metric_name
            df_values['timestamp']=df_values.apply(lambda x:self.reset_time(x.timestamp,start_time),axis=1)
            dk = dk.append(df_values)
        if metric_name in self.perf_metrics:
            dk['node'] = dk.apply(lambda x: self.evict_port(x.node), axis=1)
        
        dk['value'] = dk.apply(lambda x:self.trim_num(x.value),axis=1)
        return dk

    def system_level(self, metric_name='container_cpu_usage_seconds_total',start=1629342630,end=1629343530,step=15,namespace='openfaas-fn'):
        url = 'http://serverless.siat.ac.cn:30965/api/datasources/proxy/1/api/v1/query_range?query={metric}&start={start}&end={end}&step={step}'
        metric ='sum(rate({mtr}'.format(mtr=metric_name)+ '{namespace=~"'+ namespace +'"}[20s])) by (pod) * on(pod) group_right kube_pod_container_info'
        if metric_name =='container_memory_rss':
            metric ='sum({mtr}'.format(mtr=metric_name)+ '{namespace=~"'+ namespace +'"}) by (pod)'
            
        url=url.format(metric=metric,start=start,end=end,step=step)
        print(url)
        r = requests.get(url,headers=self.headers)
        df = r.json()['data']['result']
        df = pd.json_normalize(df)
        dk = pd.DataFrame(columns=self.system_columns)
        for i,r in df.iterrows():
            df_values = pd.DataFrame(r['values'], columns=['timestamp','value'])
            start_time = df_values['timestamp'][0]
            df_values['pod'] = r['metric.pod']
            df_values['metrics'] = metric_name
            # df_values['timestamp']=df_values.apply(lambda x:self.reset_time(x.timestamp,start_time),axis=1)
            dk = dk.append(df_values)
        dk['value'] = dk.apply(lambda x:self.trim_num(x.value),axis=1)
        return dk

    def run_prometheus_perf(self,start,end,platform,header=False,namespace='openfaas-fn'):
        start= start-30
        end = end + 30
        perf_total_df = pd.DataFrame(columns=self.columns_all)
        for m in self.perf_metrics:
            dk = self.get_perf_total(metric_name=m,start=start,end=end)
            perf_total_df = perf_total_df.append(dk)
        perf_total_df['platform']=platform
        perf_total_df.to_csv('./perf/prometheus_perf_'+platform+'.csv',index=False,header=header)
        
        perf_total_df = pd.DataFrame()
        for m in self.system_level_metrics:
            dk = self.system_level(
                metric_name=m, start=start, end=end, namespace=namespace)
            perf_total_df = perf_total_df.append(dk)
        perf_total_df['platform']=platform
        perf_total_df.to_csv('./perf/prometheus_system_'+platform+'.csv',index=False,header=header)


# prom = Prometheus()
# prom.run_prometheus_perf(start= 1636101435.5926323-30,end=1636103235.0917916,platform="Kubeless",namespace='kl')
# prom.run_prometheus_perf(start= 1636101435.5926323-30,end=1636103235.0917916,platform="Kubeless",namespace='kl')
# prom.run_prometheus_perf(start=1636101435.5926323-30,
#                          end=1636103235.0917916, platform="Kubeless", namespace='kl')

# count(kube_pod_container_info{origin_prometheus=~"$origin_prometheus", container=~"$Container", container != "", container != "POD", namespace=~"$NameSpace"}) by(container) - 0
# 