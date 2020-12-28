import pickle
import time

from sklearn.datasets import make_blobs
from sklearn.linear_model import SGDClassifier


def main(args):
    cls_name = "SGDClassifier"
    startTime = time.time()

    n_samples = args.get("n_samples", 8000)
    # we create 1000 separable points
    X, Y = make_blobs(n_samples=n_samples, centers=2, random_state=0, cluster_std=0.60)

    # fit the model
    clf = SGDClassifier(loss="hinge", alpha=0.01, max_iter=200)

    clf.fit(X, Y)
    with open("../models/{}".format(cls_name), "wb") as model:
        pickle.dump(clf, model)

main({})