from pyglet.resource import file
import random


def split(filename):
    fp = file(filename, 'rb')
    buf = fp.read(128 * 1024 * 1024)
    with open('../../BigData/openwhisk/data/train.txt', 'wb') as f:
        f.write(buf)


def split_into_random(fileName):

    for i in range(300):
        fp = file(fileName, 'rb')
        size = random.randint(1, 30)
        buf = fp.read(size * 20 * 1024)
        with open('stream_data/' + str(i), 'wb') as f:
            f.write(buf)


split('multinli_1.0_train.txt')
split_into_random('multinli_1.0_train.txt')
