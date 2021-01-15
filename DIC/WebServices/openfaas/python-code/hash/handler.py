import time
import json

def handle(args):
    startTime = time.time()
    try:
        obj = args.get("array", "hashtest")
    except AttributeError:
        obj = "hashtest"
        pass
    #obj = args.get("array", "hashtest")
    token = str(hash(obj))
    return json.dumps({'token': token, 'startTime': int(round(startTime * 1000))})
