import hashlib
import os
import time


def main(args):
    global token
    startTime = time.time()
    array = args.get("level")
    if array == "file":
        file_path = './ccf.pdf'
        if os.path.isfile(file_path):
            f = open(file_path, 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            f.close()
            token = str(hash_code).lower()
    return {'token': token, 'startTime': int(round(startTime * 1000))}
