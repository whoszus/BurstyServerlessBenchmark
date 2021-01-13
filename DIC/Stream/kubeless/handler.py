import time
from collections import Counter
from urllib import request
import random

def handler(event, context):
    startTime = time.time()
    url = 'http://172.16.101.131:10000/files/stream_data/{i}'.format(i=random.randint(0, 299))
    filedata = request.urlopen(url)
    Counter(filedata.read().strip().split())
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}
