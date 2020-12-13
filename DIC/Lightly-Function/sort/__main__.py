from sort import quicksort
def main(args):
    arr = args.get("arr",[3,6,8,10,1,2,1])
    result = quicksort(arr)
    result = str(result)
    return {"result": result}