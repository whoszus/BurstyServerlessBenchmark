from sklearn.decomposition import PCA
from sklearn.datasets import make_s_curve
from sklearn.model_selection import train_test_split
import time
import numpy as np
import scipy


def main(args):
    n_samples = args.get("n_samples", 2000)
    startTime = time.time()
    rng = np.random.RandomState(0)
    X, y = make_s_curve(n_samples=n_samples, random_state=rng)
    X = scipy.sparse.csr_matrix(X)
    X_train, X_test, _, y_test = train_test_split(X, y, random_state=rng)
    pca = PCA(n_components=150, svd_solver='randomized', whiten=True).fit(X_train)
    return {'token': 'pca finished', 'startTime': int(round(startTime * 1000))}
