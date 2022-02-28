import time


def main(args):
    startTime = time.time()

    arr = args.get("array", [3, 6, 8, 10, 1, 2, 1, 4, 5, 6, 7, 8, 2232, 2, 4, 5, 7, 9, 20, 0, 88, 7, 34])
    result = quicksort(arr)
    token = str(result)
    return {'token': token, 'startTime': startTime}


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


print(main({}))
