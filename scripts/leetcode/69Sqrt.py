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
            g=(g+x/g)/2
        return math.floor(g)



if __name__ == '__main__':
    s = Solution2()
    r = s.mySqrt(2009297850)
    print(r)
    embed()
    pass