import time
import numpy
import pickle
import json
import joblib as joblib #add this package

def handle(args):
    startTime = time.time()
    model_path = "./function/model/SGDRegressor-general"
    data_path = "./function/data/SGDRegressor-general"
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)
    clf.predict(data)

    return json.dumps({'token':  'inference finished', 'startTime': int(round(startTime * 1000))})