#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: 54SpiralMatrix.py
@time: 2018/11/30
"""
import numpy as np


class Solution(object):
    """
    给定一个包含 m x n 个元素的矩阵（m 行, n 列），请按照顺时针螺旋顺序，返回矩阵中的所有元素。

    示例 1:

    输入:
    [
     [ 1, 2, 3 ],
     [ 4, 5, 6 ],
     [ 7, 8, 9 ]
    ]
    输出: [1,2,3,6,9,8,7,4,5]
    示例 2:

    输入:
    [
      [1, 2, 3, 4],
      [5, 6, 7, 8],
      [9,10,11,12]
    ]
    输出: [1,2,3,4,8,12,11,10,9,5,6,7]
    """
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        pass


def spiral(matrix):
    if not matrix:
        return []
    matrix = np.array(matrix)
    a = matrix[0:1]
    a = a.reshape()
    b = matrix[1:, -1:]
    c = matrix[-1:, :-1]
    d = matrix[-2: 1, 0:1]

    matrix = matrix[1: -2, 1:-2]
    spiral(matrix)


if __name__ == '__main__':
    if 1:
        m = [[1, 2, 3, 4, 5, 6, 7, ],
             [20, 21, 22, 23, 24, 25, 8, ],
             [19, 32, 33, 34, 35, 26, 9, ],
             [18, 31, 30, 29, 28, 27, 10, ],
             [17, 16, 15, 14, 13, 12, 11, ],
             ]
        spiral(m)
    pass