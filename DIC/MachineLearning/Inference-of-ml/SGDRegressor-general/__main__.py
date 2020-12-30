import time
import numpy
import pickle
from sklearn.svm import SVC

from sklearn.linear_model import SGDRegressor


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)

    model_path = "/model/SGDRegressor-general"
    data_path = "/data/SGDRegressor-general"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)

    clf = SGDRegressor()
    clf.predict(data)


    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}