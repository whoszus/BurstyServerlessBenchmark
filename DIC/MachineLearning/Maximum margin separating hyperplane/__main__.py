from sklearn.linear_model import SGDClassifier
from sklearn.datasets import make_blobs
import time


def main(args):
    startTime = time.time()
    n_samples = args.get("n_samples", 1000)
    # we create 1000 separable points
    X, Y = make_blobs(n_samples=n_samples, centers=2, random_state=0, cluster_std=0.60)

    # fit the model
    clf = SGDClassifier(loss="hinge", alpha=0.01, max_iter=200)

    clf.fit(X, Y)

    return {'token': "token", 'startTime': int(round(startTime * 1000))}
