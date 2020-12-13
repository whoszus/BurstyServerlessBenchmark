def main(args):
    obj  = args.get("array","hashtest")
    return {"hash": str(hash(obj))}