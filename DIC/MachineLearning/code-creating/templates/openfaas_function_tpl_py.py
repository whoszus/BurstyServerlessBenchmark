import time
import numpy
import pickle
import json

def handle(args):
    startTime = time.time()
    model_path = "{model_path}"
    data_path = "{data_path}"
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)
    clf.predict(data)
