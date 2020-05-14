# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       121.py.py 
   Description :     
   Author :          cugxy 
   date：            2020/02/15 
-------------------------------------------------
   Change Activity:
                     2020/02/15 
-------------------------------------------------

给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

如果你最多只允许完成一笔交易（即买入和卖出一支股票），设计一个算法来计算你所能获取的最大利润。

注意你不能在买入股票前卖出股票。

示例 1:

输入: [7,1,5,3,6,4]
输出: 5
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
     注意利润不能是 7-1 = 6, 因为卖出时间需要晚于买入时间。
示例 2:

输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。

"""
import sys


class Solution:
    def maxProfit(self, prices):
        if not prices:
            return 0
        min_v = sys.maxsize
        r = 0
        for e in prices:
            if e < min_v:
                min_v = e
            elif e - min_v > r:
                r = e - min_v
        return r


if __name__ == '__main__':
    s = Solution()
    if 1:
        p3 = [2,4,1]
        print(s.maxProfit(p3))
    if 1:
        p1 = [7,1,5,3,6,1]
        print(s.maxProfit(p1))
    if 1:
        p2 = [7,6,4,3,1]
        print(s.maxProfit(p2))
    pass
