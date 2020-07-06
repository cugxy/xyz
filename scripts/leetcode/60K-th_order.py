# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       60K-th_order.py 
   Description :     
   Author :          cugxy 
   date：            2020/7/6 
-------------------------------------------------
   Change Activity:
                     2020/7/6 
-------------------------------------------------

给出集合 [1,2,3,…,n]，其所有元素共有 n! 种排列。

按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下：

"123"
"132"
"213"
"231"
"312"
"321"
给定 n 和 k，返回第 k 个排列。

说明：

给定 n 的范围是 [1, 9]。
给定 k 的范围是[1,  n!]。
示例 1:

输入: n = 3, k = 3
输出: "213"
示例 2:

输入: n = 4, k = 9
输出: "2314"

"""

__author__ = 'cugxy'

import math


class Solution:

    def fact(self, n):
        s = 1
        for i in range(1, n + 1):
            s = i * s
        return s

    def getPermutation(self, n: int, k: int) -> str:
        num = [i for i in range(1, n+1)]
        rs = []
        n_ = n
        for i in range(0, n):
            f = self.fact(n_ - 1)
            kf = k / f
            if kf == int(kf):
                kf = kf - 1
            idx = int(kf)
            rs.append(num[idx])
            num.pop(idx)
            k = k - f
            n_ = n_ - 1
            if k <= 0:
                break
        if len(rs) != n:
            for i in range(1, n + 1):
                if i not in rs:
                    rs.append(i)
        rs = [str(e) for e in rs]
        return ''.join(rs)


if __name__ == '__main__':
    if 1:
        s = Solution()
        r = s.getPermutation(4, 9)
        print(r)

