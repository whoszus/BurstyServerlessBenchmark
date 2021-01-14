from collections import Counter
import time
import random
from urllib import request

def main(args):

    startTime = time.time()
    url = 'http://172.169.8.254:10000/files/stream_data/{i}'.format(i=random.randint(0, 299))
    filedata = request.urlopen(url)
    Counter(filedata.read().strip().split())
    # for key, value in count.most_common(100):
    #     print(key + " - " + str(value))
    return {'token': 'inference finished', 'startTime': int(round(startTime * 1000))}

