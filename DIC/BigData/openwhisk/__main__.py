from collections import Counter
import time
from urllib import request

def main(args):
    startTime = time.time()
    url = 'http://172.169.8.254:10000/files/bbserverless/bigdata/train.txt'
    filedata = request.urlopen(url)
    Counter(filedata.read().strip().split())
    return {'token': 'inference finished', 'startTime': startTime}