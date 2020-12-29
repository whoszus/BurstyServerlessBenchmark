import itertools
import os.path
import pickle
import re
import sys
import tarfile
import time
from glob import glob
from html.parser import HTMLParser
from urllib.request import urlretrieve

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB

scal = 'general'


partial_fit_classifiers = {
    'TEXT-SGD-{}'.format(scal): SGDClassifier(max_iter=5),
    'TEXT-Perceptron-{}'.format(scal): Perceptron(),
    'TEXT-NB-Multinomial-{}'.format(scal): MultinomialNB(alpha=0.01),
    'TEXT-Passive-Aggressive-{}'.format(scal): PassiveAggressiveClassifier(),
}


def _not_in_sphinx():
    # Hack to detect whether we are running by the sphinx builder
    return '__file__' in globals()


class ReutersParser(HTMLParser):
    """Utility class to parse a SGML file and yield documents one at a time."""

    def __init__(self, encoding='latin-1'):
        HTMLParser.__init__(self)
        self._reset()
        self.encoding = encoding

    def handle_starttag(self, tag, attrs):
        method = 'start_' + tag
        getattr(self, method, lambda x: None)(attrs)

    def handle_endtag(self, tag):
        method = 'end_' + tag
        getattr(self, method, lambda: None)()

    def _reset(self):
        self.in_title = 0
        self.in_body = 0
        self.in_topics = 0
        self.in_topic_d = 0
        self.title = ""
        self.body = ""
        self.topics = []
        self.topic_d = ""

    def parse(self, fd):
        self.docs = []
        for chunk in fd:
            self.feed(chunk.decode(self.encoding))
            for doc in self.docs:
                yield doc
            self.docs = []
        self.close()

    def handle_data(self, data):
        if self.in_body:
            self.body += data
        elif self.in_title:
            self.title += data
        elif self.in_topic_d:
            self.topic_d += data

    def start_reuters(self, attributes):
        pass

    def end_reuters(self):
        self.body = re.sub(r'\s+', r' ', self.body)
        self.docs.append({'title': self.title,
                          'body': self.body,
                          'topics': self.topics})
        self._reset()

    def start_title(self, attributes):
        self.in_title = 1

    def end_title(self):
        self.in_title = 0

    def start_body(self, attributes):
        self.in_body = 1

    def end_body(self):
        self.in_body = 0

    def start_topics(self, attributes):
        self.in_topics = 1

    def end_topics(self):
        self.in_topics = 0

    def start_d(self, attributes):
        self.in_topic_d = 1

    def end_d(self):
        self.in_topic_d = 0
        self.topics.append(self.topic_d)
        self.topic_d = ""


def stream_reuters_documents(data_path="./reuters"):
    """Iterate over documents of the Reuters dataset.

    The Reuters archive will automatically be downloaded and uncompressed if
    the `data_path` directory does not exist.

    Documents are represented as dictionaries with 'body' (str),
    'title' (str), 'topics' (list(str)) keys.

    """

    DOWNLOAD_URL = ('http://archive.ics.uci.edu/ml/machine-learning-databases/'
                    'reuters21578-mld/reuters21578.tar.gz')
    ARCHIVE_FILENAME = 'reuters21578.tar.gz'

    if not os.path.exists(data_path):
        """Download the dataset."""
        print("downloading dataset (once and for all) into %s" %
              data_path)
        os.mkdir(data_path)

        def progress(blocknum, bs, size):
            total_sz_mb = '%.2f MB' % (size / 1e6)
            current_sz_mb = '%.2f MB' % ((blocknum * bs) / 1e6)
            if _not_in_sphinx():
                sys.stdout.write(
                    '\rdownloaded %s / %s' % (current_sz_mb, total_sz_mb))

        archive_path = os.path.join(data_path, ARCHIVE_FILENAME)
        urlretrieve(DOWNLOAD_URL, filename=archive_path,
                    reporthook=progress)
        if _not_in_sphinx():
            sys.stdout.write('\r')
        print("untarring Reuters dataset...")
        tarfile.open(archive_path, 'r:gz').extractall(data_path)
        print("done.")

    parser = ReutersParser()
    for filename in glob(os.path.join(data_path, "*.sgm")):
        for doc in parser.parse(open(filename, 'rb')):
            yield doc


def main():
    vectorizer = HashingVectorizer(decode_error='ignore', n_features=2 ** 18,
                                   alternate_sign=False)

    # Iterator over parsed Reuters SGML files.
    data_stream = stream_reuters_documents()

    # We learn a binary classification between the "acq" class and all the others.
    # "acq" was chosen as it is more or less evenly distributed in the Reuters
    # files. For other datasets, one should take care of creating a test set with
    # a realistic portion of positive instances.
    all_classes = np.array([0, 1])
    positive_class = 'acq'

    # Here are some classifiers that support the `partial_fit` method

    def get_minibatch(doc_iter, size, pos_class=positive_class):
        """Extract a minibatch of examples, return a tuple X_text, y.

        Note: size is before excluding invalid docs with no topics assigned.

        """
        data = [('{title}\n\n{body}'.format(**doc), pos_class in doc['topics'])
                for doc in itertools.islice(doc_iter, size)
                if doc['topics']]
        if not len(data):
            return np.asarray([], dtype=int), np.asarray([], dtype=int)
        X_text, y = zip(*data)
        return X_text, np.asarray(y, dtype=int)

    def iter_minibatches(doc_iter, minibatch_size):
        """Generator of minibatches."""
        X_text, y = get_minibatch(doc_iter, minibatch_size)
        while len(X_text):
            yield X_text, y
            X_text, y = get_minibatch(doc_iter, minibatch_size)

    # test data statistics
    test_stats = {'n_test': 0, 'n_test_pos': 0}

    # First we hold out a number of examples to estimate accuracy
    n_test_documents = 1000
    tick = time.time()
    X_test_text, y_test = get_minibatch(data_stream, 1000)
    parsing_time = time.time() - tick
    tick = time.time()
    X_test = vectorizer.transform(X_test_text)
    vectorizing_time = time.time() - tick
    test_stats['n_test'] += len(y_test)
    test_stats['n_test_pos'] += sum(y_test)
    print("Test set is %d documents (%d positive)" % (len(y_test), sum(y_test)))

    def progress(cls_name, stats):
        """Report progress information, return a string."""
        duration = time.time() - stats['t0']
        s = "%20s classifier : \t" % cls_name
        s += "%(n_train)6d train docs (%(n_train_pos)6d positive) " % stats
        s += "%(n_test)6d test docs (%(n_test_pos)6d positive) " % test_stats
        s += "accuracy: %(accuracy).3f " % stats
        s += "in %.2fs (%5d docs/s)" % (duration, stats['n_train'] / duration)
        return s

    cls_stats = {}

    for cls_name in partial_fit_classifiers:
        stats = {'n_train': 0, 'n_train_pos': 0,
                 'accuracy': 0.0, 'accuracy_history': [(0, 0)], 't0': time.time(),
                 'runtime_history': [(0, 0)], 'total_fit_time': 0.0}
        cls_stats[cls_name] = stats

    get_minibatch(data_stream, n_test_documents)
    # Discard test set

    # We will feed the classifier with mini-batches of 1000 documents; this means
    # we have at most 1000 docs in memory at any time.  The smaller the document
    # batch, the bigger the relative overhead of the partial fit methods.
    minibatch_size = 1000

    # Create the data_stream that parses Reuters SGML files and iterates on
    # documents as a stream.
    minibatch_iterators = iter_minibatches(data_stream, minibatch_size)
    total_vect_time = 0.0

    # Main loop : iterate on mini-batches of examples
    for i, (X_train_text, y_train) in enumerate(minibatch_iterators):
        tick = time.time()
        X_train = vectorizer.transform(X_train_text)
        total_vect_time += time.time() - tick
        for cls_name, cls in partial_fit_classifiers.items():
            cls.partial_fit(X_train, y_train, classes=all_classes)
            with open("../models/{}".format(cls_name), "wb") as model:
                pickle.dump(cls, model)

            with open("../testData/{}".format(cls_name), "wb") as test_data:
                pickle.dump(X_test, test_data)

            print(cls.score(X_test, y_test))


main()
