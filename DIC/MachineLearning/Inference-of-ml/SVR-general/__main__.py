import time
import numpy
import pickle
from sklearn.svm import SVC

from sklearn.svm import SVR


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)

    model_path = "/model/SVR-general"
    data_path = "/data/SVR-general"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)

    clf = SVR()
    clf.predict(data)


    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}