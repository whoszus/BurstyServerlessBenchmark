from sort import quicksort
import time


def main(args):
    startTime = time.time()

    arr = args.get("array", [3, 6, 8, 10, 1, 2, 1])
    result = quicksort(arr)
    token = str(result)
    return {'token': token, 'startTime': int(round(startTime * 1000))}
