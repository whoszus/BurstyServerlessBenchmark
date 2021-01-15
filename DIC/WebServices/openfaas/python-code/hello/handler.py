from helper import helper
import time


def handle(args):
    startTime = time.time()
    return {'token': helper(args), 'startTime': int(round(startTime * 1000))}
