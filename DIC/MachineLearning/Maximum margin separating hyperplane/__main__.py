from sklearn.linear_model import SGDClassifier
from sklearn.datasets import make_blobs


def main(args):
    n_samples = args.get("smaples", 1000)
    # we create 1000 separable points
    X, Y = make_blobs(n_samples=n_samples, centers=2, random_state=0, cluster_std=0.60)

    # fit the model
    clf = SGDClassifier(loss="hinge", alpha=0.01, max_iter=200)

    clf.fit(X, Y)

    # # plot the line, the points, and the nearest vectors to the plane
    # xx = np.linspace(-1, 5, 10)
    # yy = np.linspace(-1, 5, 10)
    #
    # X1, X2 = np.meshgrid(xx, yy)
    # Z = np.empty(X1.shape)
    # for (i, j), val in np.ndenumerate(X1):
    #     x1 = val
    #     x2 = X2[i, j]
    #     p = clf.decision_function([[x1, x2]])
    #     Z[i, j] = p[0]
    # levels = [-1.0, 0.0, 1.0]
    # linestyles = ['dashed', 'solid', 'dashed']
    # colors = 'k'
    # plt.contour(X1, X2, Z, levels, colors=colors, linestyles=linestyles)
    # plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Paired,
    #             edgecolor='black', s=20)
    #
    # plt.axis('tight')
    # plt.show()
    return {"result": "good"}


print(main({"name": "hello"}))
