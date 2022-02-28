#from helper import helper
import time


def handler(event, context):
    startTime = time.time()

    name = "stranger"
    greeting = "Hello from helper.py, " + name + "!"

    return {'token': greeting, 'startTime': startTime}
