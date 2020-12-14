import numpy as np
from sklearn.naive_bayes import MultinomialNB


def main(args):
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(6, 100))
    y = np.array([1, 2, 3, 4, 5, 6])
    clf = MultinomialNB()
    clf.fit(X, y)
    MultinomialNB()
    return {"inference result": str(clf.predict(X[2:3]))}
