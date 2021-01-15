from collections import Counter
import time


def main(args):
    startTime = time.time()
    fileName = "/data/train.txt"
    with open(fileName, encoding='utf-8') as doc:
        count = Counter(doc.read().strip().split())
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}
