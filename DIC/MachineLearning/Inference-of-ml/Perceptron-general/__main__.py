import time
import numpy
import pickle
from sklearn.svm import SVC

from sklearn.linear_model import Perceptron


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)

    model_path = "/model/Perceptron-general"
    data_path = "/data/Perceptron-general"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)

    clf = Perceptron()
    clf.predict(data)


    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}