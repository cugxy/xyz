# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       118_yanghui_triangle
   Description :
   Author :          cugxy
   date：            2019/9/24
-------------------------------------------------
   Change Activity:
                     2019/9/24
-------------------------------------------------

给定一个非负整数 numRows，生成杨辉三角的前 numRows 行。

在杨辉三角中，每个数是它左上方和右上方的数的和。

示例:

输入: 5
输出:
[
     [1],
    [1,1],
   [1,2,1],
  [1,3,3,1],
 [1,4,6,4,1]
]

"""


class Solution(object):
    def generate(self, numRows):
        """
        :type numRows: int
        :rtype: List[List[int]]
        """
        rs = []
        r = []
        for i in range(numRows):
            r = self.row(r)
            rs.append(r)
        return rs

    def getRow(self, rowIndex):
        """
        :type rowIndex: int
        :rtype: List[int]
        """
        r = []
        for i in range(rowIndex + 1):
            r = self.row(r)
        return r

    def row(self, f):
        if not f:
            return [1]
        n = len(f)
        if n == 1:
            return [1, 1]
        r = [1 for e in range(n + 1)]
        for i in range(0, n - 1):
            r[i + 1] = f[i] + f[i + 1]
        return r


if __name__ == '__main__':
    s = Solution()
    r = s.generate(5)
    print(r)
