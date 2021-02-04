import pickle
import json


def par(action_name, path):
    with open(path, 'rb') as file:
        results = pickle.load(file)
    action_runs_all_thread = []
    latencies_all_thread = []
    exceptions = 0

    for item in results:
        action_runs, latencies, exception = parse_result(action_name, item)
        action_runs_all_thread+=action_runs
        latencies_all_thread +=latencies
        exceptions += exception

    total = 0
    for latency in action_runs_all_thread:
        total += latency


# startTime = function start time;
# endTime = function return time;
# invokeTime = request time
# runs: life cycle
# schedule_latency
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
        if line.find(' "startTime": ,') != -1:
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


if __name__ == '__main__':
    par("hello", 'result.pickle')
