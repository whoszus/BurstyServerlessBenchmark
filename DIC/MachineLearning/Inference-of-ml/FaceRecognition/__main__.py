import time
import numpy
import pickle
from sklearn.svm import SVC

from sklearn.GridSearchCV import FaceRecognition


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)

    model_path = "/model/FaceRecognition"
    data_path = "/data/FaceRecognition"
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)

    clf = FaceRecognition()
    clf.predict(data)


    return {'token':  'inference finished', 'startTime': int(round(startTime * 1000))}