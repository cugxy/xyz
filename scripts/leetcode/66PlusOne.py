#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""

class Solution:
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        sum = 0
        for i in range(len(digits)):
            n = digits[i]
            sum = sum * 10 + n
        sum = sum + 1
        r = []
        while True:
            n = sum / 10
            m = sum % 10
            if n == 0:
                r.append(m)
                break
            r.append(m)
            sum = sum / 10
        r.reverse()
        return r


if __name__ == '__main__':
    s = Solution()
    r = s.plusOne([5, 2, 0, 3])
    pass