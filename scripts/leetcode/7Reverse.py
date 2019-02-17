#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""


class Solution:
    """
    给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。

    示例 1:

    输入: 123
    输出: 321
     示例 2:

    输入: -123
    输出: -321
    示例 3:

    输入: 120
    输出: 21
    注意:

    假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−231,  231 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。
    """
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