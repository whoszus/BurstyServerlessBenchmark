import numpy as np
import time


def main(args):
    n_samples = args.get("n_samples", 4000)
    n_features = args.get("n_features", 40)
    startTime = time.time()
    from sklearn.ensemble import HistGradientBoostingRegressor
    from sklearn.experimental import enable_hist_gradient_boosting  # noqa
    from sklearn.linear_model import PoissonRegressor
    from sklearn.model_selection import train_test_split
    rng = np.random.RandomState(0)
    X = rng.randn(n_samples, n_features)
    # positive integer target correlated with X[:, 5] with many zeros:
    y = rng.poisson(lam=np.exp(X[:, 5]) / 2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=rng)
    glm = PoissonRegressor()
    gbdt = HistGradientBoostingRegressor(loss='poisson', learning_rate=.01)
    glm.fit(X_train, y_train)
    gbdt.fit(X_train, y_train)
    token = "glm_score:" + str(glm.score(X_test, y_test)) + " gbdt_score:" + str(gbdt.score(X_test, y_test))
    return {'token': token, 'startTime': int(round(startTime * 1000))}
