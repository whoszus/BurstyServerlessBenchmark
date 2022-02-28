import time
from collections import Counter
from urllib import request
import json

def handle(c):
    startTime = time.time()
    url = 'http://172.169.8.254:10000/files/bbserverless/bigdata/train.txt'
    filedata = request.urlopen(url)
    Counter(filedata.read().strip().split())
    return json.dumps({'token': 'inference finished', 'startTime': startTime})
