from collections import Counter
import time


def main(args):
    startTime = time.time()
    fileName = "/data/train.txt"
    with open(fileName, encoding='utf-8') as doc:
        count = Counter(doc.read().strip().split())
    # for key, value in count.most_common(100):
    #     print(key + " - " + str(value))
    end_time = time.time()
    print(end_time -startTime)
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}


print(main({}))
