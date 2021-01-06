from cryptography.fernet import Fernet, MultiFernet
import time


def main(args):
    startTime = time.time()
    obj = args.get("crypt", "crypt test")
    obj = bytes(obj, 'utf-8')
    key1 = Fernet(Fernet.generate_key())
    key2 = Fernet(Fernet.generate_key())
    f = MultiFernet([key1, key2])
    token = f.encrypt(obj)
    return {'token': str(token), 'startTime': int(round(startTime * 1000))}
