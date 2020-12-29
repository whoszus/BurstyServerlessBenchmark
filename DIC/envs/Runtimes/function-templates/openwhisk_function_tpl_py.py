import time
import numpy
import pickle

{import_modules}


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)

    model_path = "{model_path}"
    data_path = "{data_path}"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)

    clf = {model}
    clf.predict(data)

