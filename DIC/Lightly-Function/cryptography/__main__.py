from cryptography.fernet import Fernet, MultiFernet


def main(args):
    obj = args.get("array", "hashtest")
    obj = bytes(obj, 'utf-8')
    key1 = Fernet(Fernet.generate_key())
    key2 = Fernet(Fernet.generate_key())
    f = MultiFernet([key1, key2])

    token = f.encrypt(obj)
    return {"token": str(token)}
