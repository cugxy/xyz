# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       115.py
   Description :
   Author :          cugxy
   date：            2019/10/31
-------------------------------------------------
   Change Activity:
                     2019/10/31
-------------------------------------------------

给定一个字符串 S 和一个字符串 T，计算在 S 的子序列中 T 出现的个数。

一个字符串的一个子序列是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串.
（例如，"ACE" 是 "ABCDE" 的一个子序列，而 "AEC" 不是）

示例 1:

输入: S = "rabbbit", T = "rabbit"
输出: 3
解释:

如下图所示, 有 3 种可以从 S 中得到 "rabbit" 的方案。
(上箭头符号 ^ 表示选取的字母)

rabbbit
^^^^ ^^
rabbbit
^^ ^^^^
rabbbit
^^^ ^^^
示例 2:

输入: S = "babgbag", T = "bag"
输出: 5
解释:

如下图所示, 有 5 种可以从 S 中得到 "bag" 的方案。
(上箭头符号 ^ 表示选取的字母)

babgbag
^^ ^
babgbag
^^    ^
babgbag
^    ^^
babgbag
  ^  ^^
babgbag
    ^^^
思路: 递归解决,
     递归函数 当第一个匹配上时,

"""


class SolutionTimeOut:
    """
    思路: 递归解决:
        递归条件,
    """
    def numDistinct(self, s: str, t: str) -> int:
        if not t or not s:
            return 0
        return self.fun(s, t, 0, 0)

    def fun(self, s, t, i, j):
        rs = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                rs += self.fun(s, t, i + 1, j)
                j += 1
            i += 1
        if j < len(t):
            return 0
        return rs + 1


class TreeNode:
    def __init__(self, val, level=-1, parents=None):
        self.val = val
        self.level = level
        self.parents = parents


class Solution:
    def numDistinct(self, s, t):
        if not t or not s:
            return 0
        idxs = []
        for _t in t:
            idx = self.get_idx(s, _t)
            if not idx:
                continue
            idxs.append(idx)
        if not idxs:
            return 0
        f_num = {e: 1 for e in idxs[0]}
        for level in range(len(idxs) - 1):
            f_idx = idxs[level]
            n_idx = idxs[level + 1]
            n_num = {e: 0 for e in n_idx}
            for i in f_idx:
                for j in n_idx:
                    if i < j:
                        n_num[j] += f_num[i]
            f_num = n_num
        rs = sum(f_num.values())
        return rs

    def get_idx(self, s, k):
        rs = []
        for idx, _s in enumerate(s):
            if _s == k:
                rs.append(idx)
        return rs


if __name__ == '__main__':
    ss = Solution()
    if 1:
        s = 'babgbag'
        t = 'bag'
        print(ss.numDistinct(s, t))
    if 1:
        s = 'rabbbit'
        t = 'rabbit'
        print(ss.numDistinct(s, t))
    pass









