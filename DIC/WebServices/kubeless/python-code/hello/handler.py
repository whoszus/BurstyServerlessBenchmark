#from helper import helper
import time


def handler(event, context):
    startTime = time.time()
    return {'token': helper(args), 'startTime': int(round(startTime * 1000))}

def helper(dict):
   if 'name' in dict:
       name = dict['name']
   else:
       name = "stranger"
   greeting = "Hello from helper.py, " + name + "!"
   return {"greeting": greeting}