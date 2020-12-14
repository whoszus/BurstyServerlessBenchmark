import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

def main():

    X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    Y = np.array([1, 1, 2, 2])
    # Always scale the input. The most convenient way is to use a pipeline.
    clf = make_pipeline(StandardScaler(),SGDClassifier(max_iter=1000, tol=1e-3))
    clf.fit(X, Y)

    token= str(clf.predict([[-0.8, -1]]))
    return {"result": str(token)}
