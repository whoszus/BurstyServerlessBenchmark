from cryptography.fernet import Fernet, MultiFernet
import time
import json


def handle(args):
    startTime = time.time()
    try:
        obj = args.get("array", "crypt test")
    except AttributeError:
        obj = "crypt test"
        pass
    obj = bytes(obj, 'utf-8')
    key1 = Fernet(Fernet.generate_key())
    key2 = Fernet(Fernet.generate_key())
    f = MultiFernet([key1, key2])
    token = f.encrypt(obj)
    return json.dumps({'token': str(token), 'startTime': int(round(startTime * 1000))})
