import time
from collections import Counter


def handler(event, context):
    startTime = time.time()
    fileName = "/kubeless/data/train.txt"
    with open(fileName, encoding='utf-8') as doc:
        count = Counter(doc.read().strip().split())
    # for key, value in count.most_common(100):
    #     print(key + " - " + str(value))
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}