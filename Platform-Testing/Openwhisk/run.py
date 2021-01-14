import os
import random
import string
import threading
from threading import Lock
import time

import yaml
from numpy.random import seed
import concurrent.futures

start_time = time.time()
end_time = 0

mutex = Lock()


def handler(action_name, params, client_num, times):
    # threads = []
    results = []
    exception_count = 0
    time_out = 0
    thread_time_out = 60
    for i in range(client_num):
        results.append('')

    print("starting  request")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(client_num):
            params = form_params(params)
            future = executor.submit(client, action_name, times, params, exception_count)
            try:
                return_value = future.result(timeout=thread_time_out)
                # print("handler1 return_value :", return_value)
                if return_value.__contains__("invokeTime"):
                    results.append(return_value)
            except concurrent.futures.TimeoutError:
                time_out += 1
                # print("handler timeout in {}".format(thread_time_out))
                future.cancel()

    outfile = open("result.csv", "w")
    outfile.write("action_name,invokeTime,startTime,endTime\n")

    latencies = []
    minInvokeTime = 0x7fffffffffffffff
    maxEndTime = 0
    first_invoke_time = ''

    # requests = client_num * times - exception_count

    for i in range(len(results)):
        clientResult = parseResult(results[i])
        for j in range(len(clientResult)):
            outfile.write(
                action_name + ',' + clientResult[j][0] + ',' + clientResult[j][1] + ',' + clientResult[j][2] + '\n')
            latency = int(clientResult[j][-1]) - int(clientResult[j][0])
            latencies.append(latency)

            # Find the first invoked action and the last return one.
            if int(clientResult[j][0]) < minInvokeTime:
                minInvokeTime = int(clientResult[j][0])
            if int(clientResult[j][-1]) > maxEndTime:
                maxEndTime = int(clientResult[j][-1])
    formatResult(latencies, maxEndTime - minInvokeTime, client_num, times, action_name, exception_count,
                 first_invoke_time)


def client(action_name, times, params, exception_count):
    command = "./executor.sh -a {action_name} -t {times} -p '{params}'"
    command = command.format(action_name=action_name, times=times, params=params)
    # print("client1:", command)
    r = os.popen(command)
    text = r.read()
    r.close()

    if text.__contains__("Measure start up time"):
        return text
    else:
        print("client3:", text)
        exception_count += 1
        return


def parseResult(result):
    lines = result.split('\n')
    parsedResults = []
    for line in lines:
        if line.find("invokeTime") == -1:
            continue
        parsedTimes = ['', '', '']

        i = 0
        count = 0
        while count < 3:
            while i < len(line):
                # print("parseResult while:", line)
                if line[i].isdigit():
                    parsedTimes[count] = line[i:i + 13]
                    i += 13
                    count += 1
                    continue
                i += 1

        parsedResults.append(parsedTimes)
    return parsedResults


def formatResult(latencies, duration, client, loop, action_name, exception_count, first_invoke_time):
    total_req = client * loop
    end_time = time.time()

    request_num = len(latencies)

    if request_num == 0:
        print("formatResult, All failed in {}".format(duration / 1000))
        return
    latencies.sort()
    duration = float(duration)

    total = 0
    for latency in latencies:
        total += latency
    print("\n")
    print("--result for {}, {} requests--in {}s".format(action_name, total_req, total / 1000))
    averageLatency = float(total) / request_num
    _50pcLatency = latencies[int(request_num * 0.5) - 1]
    _75pcLatency = latencies[int(request_num * 0.75) - 1]
    _90pcLatency = latencies[int(request_num * 0.9) - 1]
    _95pcLatency = latencies[int(request_num * 0.95) - 1]
    _99pcLatency = latencies[int(request_num * 0.99) - 1]

    print("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%")
    print("%.2f\t%d\t%d\t%d\t%d\t%d" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    print("throughput (n/s):\n%.2f" % (request_num / (duration / 1000)))
    print("exceptions:", exception_count)
    print("success rate: {} %".format(100 * (request_num / total_req)))

    # output result to file
    resultfile = open("eval-result.log", "a")
    resultfile.write("\n --result for {}, {} requests--in {}s".format(action_name, total_req, total / 1000))
    resultfile.write("\nstart time: {} , end_time: {}".format(str(start_time), str(end_time)))
    resultfile.write("%d requests finished in %.2f seconds\n" % (request_num, (duration / 1000)))
    resultfile.write("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%\n")
    resultfile.write("%.2f\t%d\t%d\t%d\t%d\t%d\n" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    resultfile.write("throughput (n/s):\n%.2f\n" % (request_num / (duration / 1000)))
    resultfile.write("\nexceptions:{}".format(exception_count))
    resultfile.write("\nsuccess rate: {} %".format(100 * (request_num / total_req)))
    resultfile.close()
    overview = '\n' + action_name + ',' + str(request_num) + ',' + str(start_time) + ',' + str(end_time) + ',' + str(
        averageLatency) + ',' + str(_50pcLatency) + ',' + str(_75pcLatency) + ',' + str(_90pcLatency) + ',' + str(
        _95pcLatency) + ',' + str(_99pcLatency)

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
    # def mode; limit
    mode = "single"
    limit = 100

    with open("../../DIC/envs/actions.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        lf_action = data_loaded.get("webservices")
        mf_action = data_loaded.get("MlI")
        bd_action = data_loaded.get("Big-Data")
        stream_action = data_loaded.get("Stream")

    z = lf_action.copy()
    # z.update(mf_action)
    # z.update(bd_action)
    # z.update(stream_action)
    request_threads = []

    for action_name, params in z.items():
        qps = get_qps(type="webservices", limit=100)
        t = threading.Thread(target=handler, args=(action_name, params, qps, 2))
        request_threads.append(t)

    total = len(request_threads)
    for i in range(total):
        request_threads[i].start()

    for i in range(total):
        request_threads[i].join()


main()
