#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""
from IPython import embed
import numpy as np


class Solution1:
    """
    给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。

    示例 1：

    输入: "babad"
    输出: "bab"
    注意: "aba" 也是一个有效答案。
    示例 2：

    输入: "cbbd"
    输出: "bb"
    """
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        _s = s[::-1]
        substr = get_longst_substr(s, _s)
        return substr


def get_longst_substr(str1, str2):
    """
    求最长子串
    :param str1:
    :param str2:
    :return:
    """
    if not str1 or not str2:
        return ''
    r = ''
    l_1 = len(str1)
    l_2 = len(str2)
    table = np.zeros((l_1, l_2))
    for i in range(l_1):
        e1 = str1[i]
        for j in range(l_2):
            e2 = str2[j]
            if e1 == e2:
                if i == 0 or j == 0:
                    table[i][j] = 1
                else:
                    table[i][j] = table[i - 1][j - 1] + 1
    max_count = int(table.max())
    idx = np.where(table == max_count)
    while idx[0].shape[0] != 1 and (idx[0] == idx[1]).all():
        table[idx] = 0
        max_count = int(table.max())
        if max_count == 0:
            return None
        idx = np.where(table == max_count)
    if idx[0].shape[0] == 0:
        return None
    _idx = int(idx[0][0])
    for _ in range(max_count):
        r = r + str1[_idx]
        _idx = _idx - 1
    return r


class Solution:
    def longestPalindrome(self, s):
        """
        基本思路是对任意字符串，如果头和尾相同，那么它的最长回文子串一定是去头去尾之后的部分的最长回文子串加上头和尾。如果头和尾不同，那么它的最长回文子串是去头的部分的最长回文子串和去尾的部分的最长回文子串的较长的那一个。
        P[i,j]P[i,j]表示第i到第j个字符的回文子串数
        dp[i,i]=1dp[i,i]=1
        dp[i,j]=dp[i+1,j−1]+2|s[i]=s[j]dp[i,j]=dp[i+1,j−1]+2|s[i]=s[j]
        dp[i,j]=max(dp[i+1,j],dp[i,j−1])|s[i]!=s[j]

        :param s:
        :return:
        """
        n = len(s)
        maxl = 0
        start = 0
        for i in range(n):
            if i - maxl >= 1 and s[i - maxl - 1: i + 1] == s[i - maxl - 1: i + 1][::-1]:
                start = i - maxl - 1
                maxl += 2
                continue
            if i - maxl >= 0 and s[i - maxl: i + 1] == s[i - maxl: i + 1][::-1]:
                start = i - maxl
                maxl += 1
        return s[start: start + maxl]


if __name__ == '__main__':
    s = Solution()
    _r = s.longestPalindrome("abcdbbfcba")
    print(_r)
    pass

