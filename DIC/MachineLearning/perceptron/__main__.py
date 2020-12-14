from sklearn.datasets import load_digits
from sklearn.linear_model import Perceptron


def main():
    X, y = load_digits(return_X_y=True)
    clf = Perceptron(tol=1e-3, random_state=0)
    clf.fit(X, y)
    Perceptron()
    token = clf.score(X, y)
    return {"result": str(token)}
