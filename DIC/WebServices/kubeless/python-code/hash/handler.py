import time


def handler(event, context):
    startTime = time.time()

    obj = "hashtest"
    token = str(hash(obj))
    return {'token': token, 'startTime': int(round(startTime * 1000))}
