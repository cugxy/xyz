#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: $NAME.py
@time: 2018/10/5
"""
from IPython import embed
import math


class Solution1(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        for i in range(int(x / 2) + 2):
            if i * i == x:
                return i
            if i * i > x:
                return i - 1
        return None


class Solution2(object):
    def mySqrt(self, x):
        """
        牛顿方法
        :type x: int
        :rtype: int
        """
        g = x
        while math.fabs(g * g - x) > 0.1:
            g = (g + x / g) / 2
        return math.floor(g)


def sqrt_nd(a, err):
    r = a
    while math.fabs(r * r - a) > err:
        g = (g + a / g) / 2
    return r


def lfg(a, err):
    """
    初始值为 k, 计算 曲线在 x=k 处的切线的方程的根, 用 k 表示, 则可迭代求解
    :param a:
    :param err:
    :return:
    """
    r = a
    while math.fabs(r * r * r - a) > err:
        r = ((2 * r) / 3) + (a / (3 * r * r))
    return r


if __name__ == '__main__':
    # s = Solution2()
    # r = s.mySqrt(2009297850)
    r = lfg(10, 0.1)
    print(r)
    embed()
    pass