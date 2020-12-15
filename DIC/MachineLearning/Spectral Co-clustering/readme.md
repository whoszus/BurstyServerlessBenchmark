# Perceptron

This example demonstrates the Spectral Co-clustering algorithm on the twenty newsgroups dataset. The ‘comp.os.ms-windows.misc’ category is excluded because it contains many posts containing nothing but data.

The TF-IDF vectorized posts form a word frequency matrix, which is then biclustered using Dhillon’s Spectral Co-Clustering algorithm. The resulting document-word biclusters indicate subsets words used more often in those subsets documents.

For a few of the best biclusters, its most common document categories and its ten most important words get printed. The best biclusters are determined by their normalized cut. The best words are determined by comparing their sums inside and outside the bicluster.

For comparison, the documents are also clustered using MiniBatchKMeans. The document clusters derived from the biclusters achieve a better V-measure than clusters found by MiniBatchKMeans.

## Ref

https://scikit-learn.org/stable/auto_examples/bicluster/plot_bicluster_newsgroups.html#sphx-glr-auto-examples-bicluster-plot-bicluster-newsgroups-py


~~~
Connected to pydev debugger (build 202.7319.64)
Vectorizing...
Coclustering...
Done in 1.89s. V-measure: 0.4385
MiniBatchKMeans...
Done in 2.57s. V-measure: 0.3344

Best biclusters:
----------------
bicluster 0 : 1830 documents, 2522 words
categories   : 22% comp.sys.ibm.pc.hardware, 19% comp.sys.mac.hardware, 18% comp.graphics
words        : card, pc, ram, drive, bus, mac, motherboard, port, windows, floppy

bicluster 1 : 2385 documents, 3272 words
categories   : 18% rec.motorcycles, 18% rec.autos, 15% sci.electronics
words        : bike, engine, car, dod, bmw, honda, oil, motorcycle, behanna, ysu

bicluster 2 : 1886 documents, 4236 words
categories   : 23% talk.politics.guns, 19% talk.politics.misc, 13% sci.med
words        : gun, guns, firearms, geb, drugs, banks, dyer, amendment, clinton, cdt

bicluster 3 : 1146 documents, 3261 words
categories   : 29% talk.politics.mideast, 26% soc.religion.christian, 25% alt.atheism
words        : god, jesus, christians, atheists, kent, sin, morality, belief, resurrection, marriage

bicluster 4 : 1736 documents, 3959 words
categories   : 26% sci.crypt, 23% sci.space, 17% sci.med
words        : clipper, encryption, key, escrow, nsa, crypto, keys, intercon, secure, wiretap


Process finished with exit code 0
~~~