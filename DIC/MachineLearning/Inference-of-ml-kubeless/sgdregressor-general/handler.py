import time
import pickle


def handler(event, context):
    startTime = time.time()
    model_path = "/kubeless/model/sgdregressor-general"
    data_path = "/kubeless/data/sgdregressor-general"
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)
    with open(data_path, 'rb') as d:
        data = pickle.load(d)
    clf.predict(data)


    return {'token':  'inference finished', 'startTime': startTime}