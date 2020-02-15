# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       122.py.py 
   Description :     
   Author :          cugxy 
   date：            2020/02/15 
-------------------------------------------------
   Change Activity:
                     2020/02/15 
-------------------------------------------------

给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

示例 1:

输入: [7,1,5,3,6,4]
输出: 7
解释: 在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
     随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6-3 = 3 。
示例 2:

输入: [1,2,3,4,5]
输出: 4
解释: 在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5-1 = 4 。
     注意你不能在第 1 天和第 2 天接连购买股票，之后再将它们卖出。
     因为这样属于同时参与了多笔交易，你必须在再次购买前出售掉之前的股票。
示例 3:

输入: [7,6,4,3,1]
输出: 0
解释: 在这种情况下, 没有交易完成, 所以最大利润为 0。

"""


class Solution:
    def maxProfit(self, prices):
        if not prices:
            return 0
        s_idx = 0
        pricess = []
        for idx, _ in enumerate(prices):
            p = None
            if idx == len(prices) - 1:
                p = prices[s_idx:idx+1]
                if p:
                    pricess.append(p)
                break
            if prices[idx] > prices[idx + 1]:
                p = prices[s_idx:idx + 1]
                s_idx = idx + 1
            if p:
                pricess.append(p)
        if not pricess:
            pricess.append(prices)
        rs = 0
        for prices in pricess:
            if not prices or len(prices) == 1:
                continue
            min_v = 2147483647
            r = 0
            for e in prices:
                if e < min_v:
                    min_v = e
                elif e - min_v > r:
                    r = e - min_v
            rs += r
        return rs


if __name__ == '__main__':
    s = Solution()
    if 0:
        p3 = [1,2,3,4,5]
        print(s.maxProfit(p3))
    if 0:
        p1 = [7, 1, 5, 3, 6, 1]
        print(s.maxProfit(p1))
    if 1:
        p2 = [6,1,3,2,4,7]
        print(s.maxProfit(p2))
    pass
