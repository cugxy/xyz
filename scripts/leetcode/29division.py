#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


class Solution:
    """
    给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。

    返回被除数 dividend 除以除数 divisor 得到的商。

    示例 1:

    输入: dividend = 10, divisor = 3
    输出: 3
    示例 2:

    输入: dividend = 7, divisor = -3
    输出: -2
    说明:

    被除数和除数均为 32 位有符号整数。
    除数不为 0。
    假设我们的环境只能存储 32 位有符号整数，其数值范围是 [−231,  231 − 1]。本题中，如果除法结果溢出，则返回 231 − 1。
    """
    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """
        # conver to positive number, and record result symbol
        positive = True
        n = dividend
        m = divisor
        if dividend < 0:
            n = -dividend
            positive = not positive
        if divisor < 0:
            m = -divisor
            positive = not positive
        n = bin(n)[2:]
        r = []
        y = 0
        for n_i in n:
            k = int(n_i) + (y << 1)
            if k < m:
                r.append(0)
                y = k
            else:
                r.append(1)
                y = k - m
        l = len(r)
        result = 0
        for i in range(l):
            result += (r[i] << (l - i - 1))
        if not positive:
            result = -result
        if result > ((1 << 31) - 1) or result < -(1 << 31):
            return (1 << 31) - 1
        return result


if __name__ == '__main__':
    s = Solution()
    r = s.divide(15, 3)
    pass