import time


def handle(args):
    startTime = time.time()
    obj = args.get("array", "hashtest")
    token = str(hash(obj))
    return {'token': token, 'startTime': int(round(startTime * 1000))}
