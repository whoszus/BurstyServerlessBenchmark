import os
import random
import string
import threading
import time

import yaml
from numpy.random import seed
from numpy.random import shuffle

start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
end_time = 0
exception_count=0


def handler(action_name, params, client_num, times):
    threads = []
    results = []
    for i in range(client_num):
        results.append('')

    for i in range(client_num):
        t = threading.Thread(target=client, args=(i, results, action_name, times, params))
        threads.append(t)

    # start the clients
    for i in range(client_num):
        threads[i].start()

    print("start running functions")
    for i in range(client_num):
        threads[i].join()

    print("all functions finished ")

    outfile = open("result.csv", "w")
    outfile.write("invokeTime,startTime,endTime\n")

    latencies = []
    minInvokeTime = 0x7fffffffffffffff
    maxEndTime = 0
    requests = client_num*times - exception_count
    print("------request:-------", requests)
    
    for i in range(len(results)):
        clientResult = parseResult(results[i])
        # print the result of every loop of the client
        for j in range(len(clientResult)):
            outfile.write(clientResult[j][0] + ',' + clientResult[j][1] + ',' + clientResult[j][2] + '\n')

            # Collect the latency
            latency = int(clientResult[j][-1]) - int(clientResult[j][0])
            latencies.append(latency)

            # Find the first invoked action and the last return one.
            if int(clientResult[j][0]) < minInvokeTime:
                minInvokeTime = int(clientResult[j][0])
            if int(clientResult[j][-1]) > maxEndTime:
                maxEndTime = int(clientResult[j][-1])
    formatResult(latencies, maxEndTime - minInvokeTime, client_num, times)


def client(i, results, action_name, times, params):
    command = "./handler.sh -a {action_name} -t {times} -p '{params}'"
    command = command.format(action_name=action_name, times=times, params=params)
    # print("-----------------",command)
    r = os.popen(command)
    text = r.read()
    r.close()
    if text.__contains__("Measure start up time"):
        results[i] = text
    else:
        print("exception:", text)
        exception_count +=1 


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
                if line[i].isdigit():
                    parsedTimes[count] = line[i:i + 13]
                    i += 13
                    count += 1
                    continue
                i += 1

        parsedResults.append(parsedTimes)
    return parsedResults


def formatResult(latencies, duration, client, loop):
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("------len(latencies)--------:", len(latencies))
    print("------duration--------:", duration)
    requestNum = len(latencies)
    latencies.sort()
    duration = float(duration)
    # calculate the average latency
    total = 0
    for latency in latencies:
        total += latency
    print("\n")
    print("------------------ result ---------------------")
    averageLatency = float(total) / requestNum
    _50pcLatency = latencies[int(requestNum * 0.5) - 1]
    _75pcLatency = latencies[int(requestNum * 0.75) - 1]
    _90pcLatency = latencies[int(requestNum * 0.9) - 1]
    _95pcLatency = latencies[int(requestNum * 0.95) - 1]
    _99pcLatency = latencies[int(requestNum * 0.99) - 1]
    print("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%")
    print("%.2f\t%d\t%d\t%d\t%d\t%d" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    print("throughput (n/s):\n%.2f" % (requestNum / (duration / 1000)))



    # output result to file
    resultfile = open("eval-result.log", "a")
    resultfile.write("\nstart time: " + str(start_time))
    resultfile.write("\nend time: " + str(end_time))
    resultfile.write("\n\n------------------ (concurrent)result ---------------------\n")
    resultfile.write("client: %d, loop_times: %d\n" % (client, loop))
    resultfile.write("%d requests finished in %.2f seconds\n" % (requestNum, (duration / 1000)))
    resultfile.write("latency (ms):\navg\t50%\t75%\t90%\t95%\t99%\n")
    resultfile.write("%.2f\t%d\t%d\t%d\t%d\t%d\n" % (
        averageLatency, _50pcLatency, _75pcLatency, _90pcLatency, _95pcLatency, _99pcLatency))
    resultfile.write("throughput (n/s):\n%.2f\n" % (requestNum / (duration / 1000)))



def form_params(params):
    if -1 != params.find("name"):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        params = params.format(name=name)

    if -1 != params.find('array'):
        seed(1)
        random_i = random.randrange(1, 500)
        sequence = [i for i in range(random_i)]
        shuffle(sequence)
        params = params.format(array=sequence)

    if -1 != params.find('file'):
        params = params.format(file="file")

    if -1 != params.find('crypt'):
        seed(1)
        # prepare a sequence
        random_i = random.randrange(1, 500)
        sequence = [i for i in range(random_i)]
        params = params.format(crypt=sequence)

    if -1 != params.find('n_samples'):
        seed(1)
        random_i = random.randrange(1000, 10000)
        params = params.format(n_samples=random_i)

    if -1 != params.find('n_features'):
        seed(1)
        random_i = random.randrange(50, 100)
        params = params.format(n_features=random_i)

    if -1 != params.find('n_train'):
        seed(1)
        random_i = random.randrange(1000, 10000)
        params = params.format(n_train=random_i)

    if -1 != params.find('n_test'):
        seed(1)
        random_i = random.randrange(200, 1000)
        params = params.format(n_features=random_i)

    return params


def main():
    lf_action = None
    mf_action = None
    vt_action = None
    with open("../envs/actions.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        lf_action = data_loaded.get("lightly-function")

    
    request_threads = []
    for action_name, params in lf_action.items():
        params = form_params(params)
        handler(action_name, params, 512, 2)

main()
