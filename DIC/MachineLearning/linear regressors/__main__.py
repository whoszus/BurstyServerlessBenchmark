from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.linear_model import Lasso
import numpy as np
import time

def main(args):
    startTime = time.time()

    n_samples = args.get("n_samples",3000)
    n_features = args.get("n_features",30)
    rng = np.random.RandomState(0)
    X, y = make_regression(n_samples, n_features, random_state=rng)
    sample_weight = rng.rand(n_samples)
    X_train, X_test, y_train, y_test, sw_train, sw_test = train_test_split(
        X, y, sample_weight, random_state=rng)
    reg = Lasso()
    reg.fit(X_train, y_train, sample_weight=sw_train)
    token = str(reg.score(X_test, y_test, sw_test))
    return {'token': token, 'startTime': int(round(startTime * 1000))}