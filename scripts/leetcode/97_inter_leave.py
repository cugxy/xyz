#!usr/bin/env python  
# -*- coding:utf-8 _*-
"""
给定三个字符串 s1, s2, s3, 验证 s3 是否是由 s1 和 s2 交错组成的。

示例 1:
    输入: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
    输出: true
示例 2:
    输入: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
    输出: false
"""
from IPython import embed
import numpy as np


class Solution(object):
    def isInterleave(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: bool
        """
        l1, l2, l3 = len(s1), len(s2), len(s3)
        if not l3 == l1 + l2:
            return False
        dp = np.zeros((l1+1, l2+1))
        for i in range(l1+1):
            for j in range(l2+1):
                if i == 0 and j == 0:
                    dp[i, j] = 1
                elif i > 0 and dp[i - 1, j] and s3[i+j-1] == s1[i - 1]:
                    dp[i, j] = 1
                elif j > 0 and dp[i, j - 1] and s3[i+j-1] == s2[j - 1]:
                    dp[i, j] = 1
                else:
                    dp[i, j] = 0
        return True if dp[l1, l2] else False


if __name__ == '__main__':
    s = Solution()
    s1 = 'aabcc'
    s2 = 'dbbca'
    s3 = 'aadbbcbcac'
    s4 = 'aadbbbaccc'

    r = s.isInterleave(s1, s2, s4)
    print(r)
    pass
