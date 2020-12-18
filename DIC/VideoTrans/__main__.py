from transcoding import Transcoder
import time


def main(args):
    startTime = time.time()

    t = Transcoder('./MIT_2020_Vision_Part_1_300k.mp4', './result.mp4')
    t.transcode()
    return {'token': "token", 'startTime': int(round(startTime * 1000))}
