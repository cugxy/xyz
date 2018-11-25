#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""


class Solution:
    max_v = 2147483647
    min_v = -2147483648

    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        n = abs(x)
        plus = True
        if x < 0:
            plus = False
        result = 0
        while n > 0:
            pop = n % 10
            n /= 10
            temp = result * 10 + pop
            result = temp
            if plus:
                if result > self.max_v:
                    return 0
            else:
                if (-result) < self.min_v:
                    return 0
        if plus:
            return result
        else:
            return -result


if __name__ == '__main__':
    s = Solution()
    r = s.reverse(123)
    pass