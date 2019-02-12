#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: solveQueens.py
@time: 2018/12/7
"""


class Solution(object):
    """
    给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。
    每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。
    输入: 4
    输出: [
     [".Q..",  // 解法 1
      "...Q",
      "Q...",
      "..Q."],

     ["..Q.",  // 解法 2
      "Q...",
      "...Q",
      ".Q.."]
    ]
    解释: 4 皇后问题存在两个不同的解法。
    """
    N = 0
    arr = []
    result = 0

    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """
        self.N = n
        self.arr = [0 for _ in range(n)]
        self.result = 0
        self.queen(0)
        return self.result

    def queen(self, n):
        """
        放置第n列皇后的回溯函数,参数n表示第n列(从0开始)
        :param n:
        :return:
        """
        if self.N == n:
            self.print()
            return
        for i in range(self.N):
            self.arr[n] = i
            if self.check(n):
                self.queen(n + 1)

    def check(self, n):
        """
        判断第n列放置的皇后是否与前面的冲突
        :param n:
        :return:
        """
        for i in range(n):
            if self.arr[n] == self.arr[i] or abs((self.arr[n]-self.arr[i])) == abs((n-i)):
                return False
        return True

    def print(self):
        self.result += 1


if __name__ == '__main__':
    s = Solution()
    r = s.solveNQueens(4)
    print(r)
    pass