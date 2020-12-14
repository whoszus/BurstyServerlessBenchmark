# Naive Bayes text classification

multinomial Naive Bayes or *multinomial NB* model, a probabilistic learning method. The probability of a document ![$d$](https://nlp.stanford.edu/IR-book/html/htmledition/img354.png) being in class ![$c$](https://nlp.stanford.edu/IR-book/html/htmledition/img252.png) is computed as: 


$$
P(c \mid d) \propto P(c) \prod_{1 \leq k \leq n_{d}} P\left(t_{k} \mid c\right)
$$
where ![$P(\tcword_\tcposindex\vert c)$](https://nlp.stanford.edu/IR-book/html/htmledition/img866.png) is the conditional probability of term ![$\tcword_\tcposindex$](https://nlp.stanford.edu/IR-book/html/htmledition/img867.png) occurring in a document of class ![$c$](https://nlp.stanford.edu/IR-book/html/htmledition/img252.png).[![[*\]](http://nlp.stanford.edu/IR-book/html/icons/footnote.png)](https://nlp.stanford.edu/IR-book/html/htmledition/footnode.html#foot16273)We interpret ![$P(\tcword_\tcposindex\vert c)$](https://nlp.stanford.edu/IR-book/html/htmledition/img866.png) as a measure of how much evidence ![$\tcword_\tcposindex$](https://nlp.stanford.edu/IR-book/html/htmledition/img867.png) contributes that ![$c$](https://nlp.stanford.edu/IR-book/html/htmledition/img252.png) is the correct class. ![$P(c)$](https://nlp.stanford.edu/IR-book/html/htmledition/img870.png) is the prior probability of a document occurring in class ![$c$](https://nlp.stanford.edu/IR-book/html/htmledition/img252.png). If a document's terms do not provide clear evidence for one class versus another, we choose the one that has a higher prior probability. ![$\langle \tcword_1,\tcword_2,\ldots,\tcword_{n_d}\rangle$](https://nlp.stanford.edu/IR-book/html/htmledition/img871.png) are the tokens in ![$d$](https://nlp.stanford.edu/IR-book/html/htmledition/img354.png) that are part of the vocabulary we use for classification and ![$n_d$](https://nlp.stanford.edu/IR-book/html/htmledition/img872.png) is the number of such tokens in ![$d$](https://nlp.stanford.edu/IR-book/html/htmledition/img354.png). For example, ![$\langle \tcword_1,\tcword_2,\ldots,\tcword_{n_d}\rangle$](https://nlp.stanford.edu/IR-book/html/htmledition/img871.png) for the one-sentence document Beijing and Taipei join the WTO might be ![$\langle \term{Beijing}, \term{Taipei}, \term{join}, \term {WTO}\rangle $](https://nlp.stanford.edu/IR-book/html/htmledition/img873.png), with ![$n_d=4$](https://nlp.stanford.edu/IR-book/html/htmledition/img874.png), if we treat the terms and and the as stop words.

In text classification, our goal is to find the *best* class for the document. The best class in NB classification is the most likely or *maximum a posteriori* ( *MAP* ) class ![$c_{map}$](https://i.loli.net/2020/12/14/brFYS7UpdHMjyZh.png):
$$
\mathrm{c}_{\operatorname{map}}=\arg \max _{c \in \mathbb{C}} \hat{P}(c \mid d)=\arg \max _{c \in \mathbf{C}} \hat{P}(c) \Pi_{1 \leq k \leq n_{d}} \hat{P}\left(t_{k} \mid c\right)
$$
We write ![$\hat{P}$](https://nlp.stanford.edu/IR-book/html/htmledition/img877.png) for ![$P$](https://nlp.stanford.edu/IR-book/html/htmledition/img115.png) because we do not know the true values of the parameters ![$P(\tcjclass)$](https://nlp.stanford.edu/IR-book/html/htmledition/img878.png) and ![$P(\tcword_\tcposindex\vert\tcjclass)$](https://nlp.stanford.edu/IR-book/html/htmledition/img879.png), but estimate them from the training set as we will see in a moment.







## Ref

https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html