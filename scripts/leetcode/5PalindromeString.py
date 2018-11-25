#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""
from IPython import embed
import numpy as np


def get_longst_substr(str1, str2):
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
        :type s: str
        :rtype: str
        """
        _s = s[::-1]
        substr = get_longst_substr(s, _s)
        return substr

if __name__ == '__main__':
    s = Solution()
    r = s.longestPalindrome("abcgba")
    embed()
    pass

