import time

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.metrics import completeness_score
from sklearn.preprocessing import StandardScaler


def main(args):
    n_samples = args.get("n_samples", 4000)
    rng = np.random.RandomState(0)
    startTime = time.time()

    # Generate sample data
    X, labels_true = make_blobs(n_samples=n_samples, cluster_std=0.4, random_state=rng)

    X = StandardScaler().fit_transform(X)

    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    token = completeness_score(labels, labels_true)
    return {'token': token, 'startTime': int(round(startTime * 1000))}
