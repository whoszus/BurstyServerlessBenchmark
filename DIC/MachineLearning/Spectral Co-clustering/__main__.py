from collections import defaultdict
import operator
from time import time

import numpy as np

from sklearn.cluster import SpectralCoclustering
from sklearn.cluster import MiniBatchKMeans
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.cluster import v_measure_score


def number_normalizer(tokens):
    """ Map all numeric tokens to a placeholder.

    For many applications, tokens that begin with a number are not directly
    useful, but the fact that such a token exists can be relevant.  By applying
    this form of dimensionality reduction, some methods may perform better.
    """
    return ("#NUMBER" if token[0].isdigit() else token for token in tokens)


class NumberNormalizingVectorizer(TfidfVectorizer):
    def build_tokenizer(self):
        tokenize = super().build_tokenizer()
        return lambda doc: list(number_normalizer(tokenize(doc)))


def bicluster_ncut(i):
    rows, cols = cocluster.get_indices(i)
    if not (np.any(rows) and np.any(cols)):
        import sys
        return sys.float_info.max
    row_complement = np.nonzero(np.logical_not(cocluster.rows_[i]))[0]
    col_complement = np.nonzero(np.logical_not(cocluster.columns_[i]))[0]
    # Note: the following is identical to X[rows[:, np.newaxis],
    # cols].sum() but much faster in scipy <= 0.16
    weight = X[rows][:, cols].sum()
    cut = (X[row_complement][:, cols].sum() +
           X[rows][:, col_complement].sum())
    return cut / weight


def most_common(d):
    """Items of a defaultdict(int) with the highest values.

    Like Counter.most_common in Python >=2.7.
    """
    return sorted(d.items(), key=operator.itemgetter(1), reverse=True)


def main(args):
    startTime = time()

    # exclude 'comp.os.ms-windows.misc'
    categories = ['alt.atheism', 'comp.graphics',
                  'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware',
                  'comp.windows.x', 'misc.forsale', 'rec.autos',
                  'rec.motorcycles', 'rec.sport.baseball',
                  'rec.sport.hockey', 'sci.crypt', 'sci.electronics',
                  'sci.med', 'sci.space', 'soc.religion.christian',
                  'talk.politics.guns', 'talk.politics.mideast',
                  'talk.politics.misc', 'talk.religion.misc']
    newsgroups = fetch_20newsgroups(categories=categories)
    y_true = newsgroups.target

    vectorizer = NumberNormalizingVectorizer(stop_words='english', min_df=5)
    cocluster = SpectralCoclustering(n_clusters=len(categories),
                                     svd_method='arpack', random_state=0)
    kmeans = MiniBatchKMeans(n_clusters=len(categories), batch_size=20000,
                             random_state=0)

    print("Vectorizing...")
    X = vectorizer.fit_transform(newsgroups.data)

    print("Coclustering...")
    start_time = time()
    cocluster.fit(X)
    y_cocluster = cocluster.row_labels_
    print("Done in {:.2f}s. V-measure: {:.4f}".format(
        time() - start_time,
        v_measure_score(y_cocluster, y_true)))

    print("MiniBatchKMeans...")
    start_time = time()
    y_kmeans = kmeans.fit_predict(X)
    print("Done in {:.2f}s. V-measure: {:.4f}".format(
        time() - start_time,
        v_measure_score(y_kmeans, y_true)))

    feature_names = vectorizer.get_feature_names()
    document_names = list(newsgroups.target_names[i] for i in newsgroups.target)

    bicluster_ncuts = list(bicluster_ncut(i)
                           for i in range(len(newsgroups.target_names)))
    best_idx = np.argsort(bicluster_ncuts)[:5]

    print()
    print("Best biclusters:")
    print("----------------")
    token = "token:"
    for idx, cluster in enumerate(best_idx):
        n_rows, n_cols = cocluster.get_shape(cluster)
        cluster_docs, cluster_words = cocluster.get_indices(cluster)
        if not len(cluster_docs) or not len(cluster_words):
            continue

        # categories
        counter = defaultdict(int)
        for i in cluster_docs:
            counter[document_names[i]] += 1
        cat_string = ", ".join("{:.0f}% {}".format(float(c) / n_rows * 100, name)
                               for name, c in most_common(counter)[:3])

        # words
        out_of_cluster_docs = cocluster.row_labels_ != cluster
        out_of_cluster_docs = np.where(out_of_cluster_docs)[0]
        word_col = X[:, cluster_words]
        word_scores = np.array(word_col[cluster_docs, :].sum(axis=0) -
                               word_col[out_of_cluster_docs, :].sum(axis=0))
        word_scores = word_scores.ravel()
        important_words = list(feature_names[cluster_words[i]]
                               for i in word_scores.argsort()[:-11:-1])

        token += str("bicluster {} : {} documents, {} words".format(
            idx, n_rows, n_cols))
        token += str("categories   : {}".format(cat_string))
        token += str("words        : {}\n".format(', '.join(important_words)))

    return {'token': token, 'startTime': int(round(startTime * 1000))}
