import time


def handler(event, context):
    startTime = time.time()
    obj = event.get("array", "hashtest")
    token = str(hash(obj))
    return {'token': token, 'startTime': int(round(startTime * 1000))}
