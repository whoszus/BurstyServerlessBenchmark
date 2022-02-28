import time
from collections import Counter
from urllib import request


def handler(event, context):
    startTime = time.time()
    url = 'http://172.169.8.254:10000/files/bbserverless/bigdata/train.txt'
    filedata = request.urlopen(url)
    count = Counter(filedata.read().strip().split())
    return {'token': 'inference finished', 'startTime': startTime}
