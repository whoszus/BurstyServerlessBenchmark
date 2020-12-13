from cryptography.fernet import Fernet, MultiFernet
def main(args):
    obj  = args.get("array","hashtest")
    key1 = Fernet(Fernet.generate_key())
    key2 = Fernet(Fernet.generate_key())
    f = MultiFernet([key1, key2])
    
    token = f.encrypt(b"Secret message!")
    return {"hash": token} ``