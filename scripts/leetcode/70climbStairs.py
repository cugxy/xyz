#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: $NAME.py
@time: 2018/10/5
"""

"""

fun(0) = 1
fun(1) = 1
fun(2) = 2
fun(3) = 3
fun(4) = 5

fun(n) = fun(n - 1) + fun(n - 2)

"""


class Solution(object):
    """
    假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
    每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
    注意：给定 n 是一个正整数。
    """
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        return self.fun(n)

    def fun(self, n):
        if n == 0:
            return 1
        if n == 1:
            return 1
        sum = self.fun(n - 1) + self.fun(n - 2)
        return sum


class Solution2(object):
     def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        lst = []
        lst.append(1)
        lst.append(1)
        for i in range(2, n + 1):
            lst.append(lst[i - 1] + lst[i - 2])
        return lst[n] 

if __name__ == '__main__':
    s = Solution2()
    r = s.climbStairs(4)
    print(r)
