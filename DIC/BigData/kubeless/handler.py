import time
from collections import Counter


def handler(event, context):
    startTime = time.time()
    fileName = "/kubeless/data/train.txt"
    with open(fileName, encoding='utf-8') as doc:
        count = Counter(doc.read().strip().split())
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}
