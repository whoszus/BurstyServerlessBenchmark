import scipy
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.datasets import make_s_curve

from sklearn.metrics import completeness_score


def main(args):
    n_samples = args.get("n_samples", 1000)
    rng = np.random.RandomState(0)
    X, y = make_s_curve(n_samples=n_samples, random_state=rng)
    X = scipy.sparse.csr_matrix(X)
    X_train, X_test, _, y_test = train_test_split(X, y, random_state=rng)
    kmeans = KMeans(algorithm='elkan').fit(X_train)
    token = completeness_score(kmeans.predict(X_test), y_test)
    return {"token": token}