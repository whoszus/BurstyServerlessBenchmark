import time


def main(args):
    startTime = time.time()
    obj = args.get("array", "hashtest")
    token = str(hash(obj))
    return {'token': token, 'startTime': startTime}
