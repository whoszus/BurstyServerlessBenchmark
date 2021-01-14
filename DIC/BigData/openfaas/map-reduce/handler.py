import time
from collections import Counter


def handle(c):
    startTime = time.time()
    fileName = "./function/data/train.txt"
    with open(fileName, encoding='utf-8') as doc:
        count = Counter(doc.read().strip().split())
    # for key, value in count.most_common(100):
    #     print(key + " - " + str(value))
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}