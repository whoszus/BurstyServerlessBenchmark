from sklearn.datasets import load_digits
from sklearn.linear_model import Perceptron
import time


def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples", 3000)
    X, y = load_digits(return_X_y=True)
    clf = Perceptron(tol=n_samples, random_state=0)
    clf.fit(X, y)
    Perceptron()
    token = str(clf.score(X, y))
    return {'token': token, 'startTime': int(round(startTime * 1000))}
