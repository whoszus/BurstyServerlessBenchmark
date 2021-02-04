import os
import random
import string
import threading
from threading import Lock
import time

import yaml
from numpy.random import seed
import concurrent.futures
import random
import json


def handler(action_name, params, client_num, times):
    start_time = time.time()

    threads = []
    results = []
    exceptions = 0
    action_runs_all_thread = []
    latencies_all_thread = []
    print("starting  request")

    for i in range(client_num):
        t = threading.Thread(target=client_1, args=(results, action_name, times, params))
        threads.append(t)

    # start the clients
    for i in range(client_num):
        threads[i].start()

    print("start running functions")

    for i in range(client_num):
        threads[i].join()

    print("all functions finished ")

    for item in results:
        action_runs, latencies, exception = parse_result(action_name, item)
        action_runs_all_thread += action_runs
        latencies_all_thread += latencies
        exceptions += exception

    formatResult(action_runs_all_thread, client_num, times, action_name, exceptions, start_time)


def parse_result(action_name, result):
    lines = result.split('\n')
    # parsed_results = []
    action_runs = []
    latencies = []
    exception = 0
    for line in lines:
        if line.find("invokeTime") == -1:
            continue

        parsed_times = ['', '', '']
        line = line.replace("\'", '"')
        line = line.replace("'", '"')
        if line.find('"startTime": ,') != -1:
            exception += 1
            continue
        pas = json.loads(line)
        runs = int(pas["endTime"]) - int(pas["invokeTime"])
        schedule_latency = int(pas["startTime"]) - int(pas["invokeTime"])
        action_runs.append(runs)
        latencies.append(schedule_latency)
        parsed_times[0] = pas["invokeTime"]
        parsed_times[1] = pas["startTime"]
        parsed_times[2] = pas["endTime"]

        with open("result.csv", "a+") as file:
            file.write(action_name + ',' + str(pas["invokeTime"]) + ',' + str(pas["startTime"]) + ',' + str(
                pas["endTime"]) + '\n')
        # parsed_results.append(parsed_times)

    return action_runs, latencies, exception


def client_1(result, action_name, times, params):
    print("exec ", action_name)
    command = "./executor.sh -a {action_name} -t {times} -p '{params}'"
    command = command.format(action_name=action_name, times=times, params=params)
    # print("client1:", command)
    r = os.popen(command)
    text = r.read()
    r.close()

    if text.__contains__("Measure start up time"):
        result.append(text)


def formatResult(latencies, client, loop, action_name, exception_count, start_time):
    total_req = client * loop
    end_time = time.time()
    request_num = len(latencies)
    latencies.sort()
    total = 0
    for latency in latencies:
        total += latency
    duration = end_time - start_time
    print("\n")
    print("--result for {}, {} requests--in {}s".format(action_name, total_req, duration))
    averageLatency = total / request_num
    _50pcLatency = latencies[int(request_num * 0.5) - 1]
    _75pcLatency = latencies[int(request_num * 0.75) - 1]
    _90pcLatency = latencies[int(request_num * 0.9) - 1]
    _95pcLatency = latencies[int(request_num * 0.95) - 1]
    _99pcLatency = latencies[int(request_num * 0.99) - 1]

    print("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%")
    print("%.2f\t%d\t%d\t%d\t%d\t%d" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    print("throughput (n/s):\n%.2f" % (request_num / duration))
    print("exceptions:", exception_count)
    print("failure rate: {} %".format(100 * (exception_count / total_req)))

    # output result to file
    resultfile = open("eval-result.log", "a")
    resultfile.write("\n --result for {}, {} requests--in {}s".format(action_name, total_req, total / 1000))
    resultfile.write("\nstart time: {} , end_time: {}".format(str(start_time), str(end_time)))
    resultfile.write("%d requests finished in %.2f seconds\n" % (request_num, duration))
    resultfile.write("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%\n")
    resultfile.write("%.2f\t%d\t%d\t%d\t%d\t%d\n" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    throughput = request_num / duration
    resultfile.write("throughput (n/s):\n%.2f\n" % (throughput))
    resultfile.write("\nexceptions:{}".format(exception_count))
    failure_rate = exception_count / total_req
    resultfile.write("\nfailure rate: {} %".format(100 * (failure_rate)))
    resultfile.close()
    overview = '\n' + action_name + ',' + str(total_req) + ',' + str(start_time) + ',' + str(end_time) + ',' + str(
        averageLatency) + ',' + str(_50pcLatency) + ',' + str(_75pcLatency) + ',' + str(_90pcLatency) + ',' + str(
        _95pcLatency) + ',' + str(_99pcLatency) + ',' + str(throughput) + ',' + str(failure_rate)

    with open("overview.csv", "a+") as f:
        f.write(overview)


def form_params(params):
    if -1 != params.find("name"):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        params = params.format(name=name)

    if -1 != params.find('file'):
        params = params.format(file="file")

    if -1 != params.find('crypt'):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=77))
        params = params.format(crypt=name)

    if -1 != params.find('n_samples'):
        seed(1)
        random_samples = random.randrange(1000, 10000)
        if -1 != params.find('n_features'):
            seed(1)
            random_f = random.randrange(50, 100)
            params = params.format(n_features=random_f, n_samples=random_samples)
        else:
            params = params.format(n_samples=random_samples)

    if -1 != params.find('n_train'):
        seed(1)
        random_i = random.randrange(1000, 10000)
        if -1 != params.find('n_test'):
            seed(1)
            random_t = random.randrange(200, 1000)
            random_f = random.randrange(50, 100)
            params = params.format(n_test=random_t, n_train=random_i, n_features=random_f)
        else:
            params = params.format(n_train=random_i)

    return params


def get_qps(type="webservices", mode="single", limit=100):
    t = {
        "webservices": 5,
        "MlI": 8,
        "Big-Data": 1,
        "Stream": 1,
    }
    m = {
        "webservices": 0.5,
        "MlI": 0.125,
        "Big-Data": 0.125,
        "Stream": 0.25,
    }
    r = t[type]
    k = m[type]

    if mode == "single":
        return int(limit / r)
    if mode == "mix":
        return int(limit / r * k)


def main():
    mode = "mix"
    radio = 0.5
    limit_qps = int(3000 * radio)
    loop_per_thread = 3

    with open("../../DIC/envs/actions.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        lf_action = data_loaded.get("webservices")
        mf_action = data_loaded.get("MlI")
        bd_action = data_loaded.get("Big-Data")
        stream_action = data_loaded.get("Stream")

    request_threads = []

    for action_name, params in lf_action.items():
        qps = get_qps(type="webservices", limit=limit_qps, mode=mode)
        t = threading.Thread(target=handler, args=(action_name, params, qps, loop_per_thread))
        request_threads.append(t)
    for action_name, params in mf_action.items():
        qps = get_qps(type="MlI", limit=limit_qps, mode=mode)
        t = threading.Thread(target=handler, args=(action_name, params, qps, loop_per_thread))
        request_threads.append(t)
    for action_name, params in bd_action.items():
        qps = get_qps(type="Big-Data", limit=limit_qps, mode=mode)
        t = threading.Thread(target=handler, args=(action_name, params, qps, loop_per_thread))
        request_threads.append(t)
    for action_name, params in stream_action.items():
        qps = get_qps(type="Stream", limit=limit_qps, mode=mode)
        t = threading.Thread(target=handler, args=(action_name, params, qps, loop_per_thread))
        request_threads.append(t)

    random.shuffle(request_threads)
    total = len(request_threads)
    for i in range(total):
        request_threads[i].start()

    for i in range(total):
        request_threads[i].join()


main()
