#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:cugxy 
@file: 96TreeCounts.py 
@time: 2019/04/15 
"""

"""
给定一个整数 n，求以 1 ... n 为节点组成的二叉搜索树有多少种？

示例:

输入: 3
输出: 5
解释:
给定 n = 3, 一共有 5 种不同结构的二叉搜索树:

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3
"""


class Solution(object):
    def numTrees(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 0 or n == 1:
            return 1
        num = [0] * (n+1)
        num[0] = 1
        for i in range(1, n + 1):
            num[i] = 0
            for l in range(i):
                num[i] += num[l] * num[i - l - 1]
        return num[n]


if __name__ == '__main__':
    s = Solution()
    r = s.numTrees(3)
    print(r)

    pass