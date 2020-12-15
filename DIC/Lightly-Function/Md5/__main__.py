import hashlib
import os


def main(args):
    array = args.get("level")
    md5 = None
    if array == "file":
        file_path = './ccf.pdf'
        if os.path.isfile(file_path):
            f = open(file_path, 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            f.close()
            md5 = str(hash_code).lower()
    return {"md5": md5}
