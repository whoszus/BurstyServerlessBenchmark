from transcoding import Transcoder


def main(args):
    t = Transcoder('./MIT_2020_Vision_Part_1_300k.mp4', './result.mp4')
    t.transcode()