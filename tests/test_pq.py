import numpy as np
import scipy as sp

from fast_pq import FastPQ


def test_recall():
    np.random.seed(10)
    for i in range(1, 10):
        recall_at_10 = _test_recall_inner(16 * i, 8 * i, 100, 2)
        assert recall_at_10 > 0.8


def _test_recall_inner(n, d, k, dpb):
    X = np.random.randn(n, d).astype(np.float32)
    qs = np.random.randn(k, d).astype(np.float32)
    trus = sp.spatial.distance.cdist(qs, X).argmin(axis=1)
    pq = FastPQ(dims_per_block=dpb)
    data = pq.fit_transform(X)
    recall_at_10 = 0
    for q, tru in zip(qs, trus):
        dtable = pq.distance_table(q)
        top10 = dtable.estimate_distances(data).argpartition(10)[:10]
        if tru in top10:
            recall_at_10 += 1
    return recall_at_10 / k
