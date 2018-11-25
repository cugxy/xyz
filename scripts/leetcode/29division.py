#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


class Solution:
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