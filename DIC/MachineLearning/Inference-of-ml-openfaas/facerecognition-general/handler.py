import time
import numpy
import pickle
import json

def handle(args):
    startTime = time.time()
    model_path = "./function/model/facerecognition-general"
    data_path = "./function/data/facerecognition-general"
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)
    clf.predict(data)

    return json.dumps({'token':  'inference finished', 'startTime': startTime})