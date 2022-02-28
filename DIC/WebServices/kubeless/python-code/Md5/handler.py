import hashlib
import os
import time


def handler(event, context):
    global token
    startTime = time.time()
    md5_obj = hashlib.md5()
    md5_obj.update(b"user_name.....")
    hash_code = md5_obj.hexdigest()
    token = str(hash_code).lower()
    return {'token': token, 'startTime': startTime}
