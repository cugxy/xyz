# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       kd_tree.py 
   Description :     
   Author :          cugxy 
   date：            2020/8/7 
-------------------------------------------------
   Change Activity:
                     2020/8/7 
-------------------------------------------------
"""

__author__ = 'cugxy'


class KDNode(object):
    def __init__(self):
        self.father = None
        self.left = None
        self.right = None
        self.feature = None
        self.split = None

    def __str__(self):
        return "feature: %s, split: %s" % (str(self.feature), str(self.split))

    @property
    def brother(self):
        if self.father is None:
            ret = None
        else:
            if self.father.left is self:
                ret = self.father.right
            else:
                ret = self.father.left
        return ret


class KDTree(object):
    def __init__(self):
        self.root = KDNode()

    def __str__(self):
        ret = []
        i = 0
        que = [(self.root, -1)]
        while que:
            nd, idx_father = que.pop(0)
            ret.append("%d -> %d: %s" % (idx_father, i, str(nd)))
            if nd.left is not None:
                que.append((nd.left, i))
            if nd.right is not None:
                que.append((nd.right, i))
            i += 1
        return "\n".join(ret)

    def _get_median_idx(self, X, idxs, feature):
        """
        中位数
        :param X:
        :param idxs:
        :param feature:
        :return:
        """
        n = len(idxs)
        k = n // 2
        col = map(lambda i: (i, X[i][feature]), idxs)
        sorted_idxs = map(lambda x: x[0], sorted(col, key=lambda x: x[1]))
        median_idx = list(sorted_idxs)[k]
        return median_idx

    def _get_variance(self, X, idxs, feature):
        """
        计算方差
        :param X:
        :param idxs:
        :param feature:
        :return:
        """
        n = len(idxs)
        col_sum = col_sum_sqr = 0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += xi
            col_sum_sqr += xi ** 2
        return col_sum_sqr / n - (col_sum / n) ** 2

    def _choose_feature(self, X, idxs):
        m = len(X[0])
        variances = map(lambda j: (
            j, self._get_variance(X, idxs, j)), range(m))
        return max(variances, key=lambda x: x[1])[0]

    def _split_feature(self, X, idxs, feature, median_idx):
        idxs_split = [[], []]
        split_val = X[median_idx][feature]
        for idx in idxs:
            if idx == median_idx:
                continue
            xi = X[idx][feature]
            if xi < split_val:
                idxs_split[0].append(idx)
            else:
                idxs_split[1].append(idx)
        return idxs_split