#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""
from IPython import embed


class Solution:
    """
    给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。

    示例 1:

    输入: "abcabcbb"
    输出: 3
    解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
    示例 2:

    输入: "bbbbb"
    输出: 1
    解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
    示例 3:

    输入: "pwwkew"
    输出: 3
    解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
         请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
    """
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