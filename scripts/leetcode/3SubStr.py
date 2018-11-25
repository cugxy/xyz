#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""
from IPython import embed


class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        s1 = []
        r = []
        for e in s:
            if e not in s1:
                s1.append(e)
            else:
                r.append(len(s1))
                # 删掉 e 出现之前的所有，包括 e
                idx = s1.index(e)
                s1 = s1[idx+1:]
                s1.append(e)
        r.append(len(s1))
        return max(r)


if __name__ == '__main__':
    s = Solution()
    r = s.lengthOfLongestSubstring('dvdf')
    embed()
    pass