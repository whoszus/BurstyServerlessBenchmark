# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import os
import random
import threading
import time
from multiprocessing import Process

import numpy as np
import pandas as pd
import yaml
from scipy import stats
from Metrics import FunctionCount
import uuid


result_col = ['action_name', 'invokeTime', 'startTime',
              'endTime', 'req_mod', 'schedule_latency/ms', 'qps', 'config', 'platform']


reqest_col = ['time', 'req', 'platform']


result_col = ['actionName', 'invokeTime', 'startTime',
              'endTime', 'schedule_latency', 'req', 'config', 'platform']

exp_platforms = ['Kubeless']
# exp_platforms = ['OpenFaas']




# %%
def handler(action_name, qps, config):
    uuidstring = config['uuidstring']
    cwd = config['cwd']
    threads = []
    # print('starting  request")
    platform_name = config['platform_name']
    for i in range(qps):
        t = threading.Thread(target=client_1, args=( action_name, platform_name,uuidstring,cwd))
        threads.append(t)

    # start the clients
    start_time = time.time()
    config['first_req'] = start_time
    for i in range(qps):
        threads[i].start()


## UUIDstring 用于标记一次请求一次函数请求
def client_1(action_name, platform_name,uuidstring,cwd):
    command = "bash {cwd}/{platform_name}/executor.sh -a {action_name}  -P {platform_name} -u {uuidstring}"
    command = command.format(cwd=cwd,action_name=action_name,platform_name=platform_name,uuidstring=uuidstring)
    os.system(command)

# %%

def workload_generator(triffic=60,times=400):
    X = range(triffic)
    Y = []
    X1 = range(triffic, 2*triffic)
    Y1 = []
    X2 = range(2*triffic, 3*triffic)
    Y2 = []
    for k in X:
        p = stats.poisson.pmf(k, int(triffic/5)) * times
        Y.append(p)

    for k in X1:
        p = stats.poisson.pmf(k, int(triffic+triffic/4)) * times
        Y1.append(p)

    for k in X2:
        p = stats.poisson.pmf(k, int(2*triffic + triffic/2)) * times
        Y2.append(p)

    x = np.concatenate((X, X1, X2))
    y = np.concatenate((Y, Y1, Y2))
    y = list(np.floor(y))

    r1 = list(range(0, int(triffic/5)))
    r2 = list(range(triffic, int(triffic+triffic/4)))
    r3 = list(range(2*triffic, int(2*triffic + triffic/2)))

    reverse = np.concatenate((r1, r2, r3))
    y_burst = y.copy()
    y_burst_reverse = y.copy()
    for i in reverse:
        y_burst[int(i)] = 0

    for i in range(triffic*3):
        if i not in reverse:
            y_burst_reverse[i] = 0

    w=y[0:20]
    # w1 = y[0:20]
    # w= list(np.concatenate((w, w1)))
    # x = range(0,40)
    return x, w


# %%
def multi_process(actions, qps, config):
    request_threads = []
    if config['uuidstring'] == '':
        config['uuidstring']=uuid.uuid1()
    else:
        config['uuidstring'] = 'max-'+ str(uuid.uuid1())
    for action_name, params in actions.items():
        t = threading.Thread(target=handler, args=(action_name, qps, config))
        request_threads.append(t)

    random.shuffle(request_threads)
    total = len(request_threads)
    for i in range(total):
        request_threads[i].start()
    
    # for i in range(total):
    #     request_threads[i].join()


# %%
def run(qps=5, mode='normal', platform_name='OpenFaas',last_state=False,uuids=''):
    start_time = time.time()
    cwd = os.getcwd()
    config = {"qps": qps, "first_req": '', "platform_name": platform_name, "last_state":last_state,"uuidstring":uuids,"cwd":cwd}

    with open("../DIC/envs/actions.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        lf_action = data_loaded.get("webservices")
        mf_action = data_loaded.get("MlI")
        bd_action = data_loaded.get("Big-Data")
        stream_action = data_loaded.get("Stream")
    try:

        p_web = Process(target=multi_process, args=(
            lf_action, qps, config))

        p_mf = Process(target=multi_process, args=(
            mf_action, qps, config))

        p_bigdata = Process(target=multi_process, args=(
            bd_action, qps, config))

        p_stream = Process(target=multi_process, args=(
            stream_action, qps, config))

        p_web.start()
        p_mf.start()
        p_bigdata.start()
        p_stream.start()

    except Exception:
        print('error...')
    end_time = time.time()
    record = 'start_time: ' + str(start_time) + \
         'end_time: ' + str(end_time) +'\n'

    with open('record'+platform_name+'.log', 'a+') as s:
        s.write(record)


# %%
def runner(namespace, platform_name, workload, period):
    last_state = False
    # manually control.
    threads_run = []
    # start function_instance counting
    fc = FunctionCount(namespace)
    print('start counting function instance')
    fc.get_pod_in_platform(platform_name, namespace)

    max_workload=int(max(workload)) 

    # start recording request.
    for i in range(len(workload)):
        qps = int(workload[i])
        if i == len(workload):
            last_state = True
        print('qps...', qps)
        time_now = time.time()
        df_req = pd.DataFrame({"time": [time_now], "req": [qps], "platform": [platform_name]})
        df_req.to_csv("request_"+platform_name+'.csv',header=False, index=False)
        if qps < 1:
            print('skiping')
            time.sleep(period)
            continue
        if qps ==max_workload:
            uuids='max'
        else:
            uuids=''
        t = threading.Thread(target=run, args=(qps,  'normal', platform_name,last_state,uuids))
        t.start()
        
        threads_run.append(t)
        time.sleep(period)
    for t in threads_run:
        if t.is_alive() :
            t.join()

    return
    
# %%
def entry():
    from Metrics import Prometheus
    period = 5
    x, y = workload_generator(30,200)
    print(y)
    prom = Prometheus()

    platf = {
        "OpenFaas": 'openfaas-fn',
        "OpenWhisk": 'openwhisk',
        "Kubeless": 'kl'
    }

    for platform_name in exp_platforms:
        start = time.time()
        try:
            namespace = platf[platform_name]
            runner(namespace, platform_name, y, period)
        except Exception:
            end = time.time()
        end = time.time()
        prom.run_prometheus_perf(start=start, end=end,
                                 platform=platform_name, namespace=namespace)

        with open('runTime.log','w') as f:
            string = 'platform:'+ platform_name, '+ start:'+ str(start), '+ end:'+ str(end)
            f.write(string)
            f.write("---")

# %%
os.chdir(os.path.dirname(__file__))
print(os.getcwd()) 
entry()