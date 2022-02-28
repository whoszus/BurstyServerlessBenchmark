#from helper import helper
import time
import json

def handle(args):
    startTime = time.time()

    if 'name' in args:
       name = args['name']
    else:
       name = "stranger"
    greeting = "Hello from helper.py, " + name + "!"

    return json.dumps({'token': greeting, 'startTime': startTime})