#!usr/bin/env python  
# -*- coding:utf-8 _*-
"""
判断一个 9x9 的数独是否有效。只需要根据以下规则，验证已经填入的数字是否有效即可。

数字 1-9 在每一行只能出现一次。
数字 1-9 在每一列只能出现一次。
数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。

数独部分空格内已填入了数字，空白格用 '.' 表示
@author:
@file:  
@time:  
"""
import numpy as np

class Solution:
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        sudoku_1 = np.array(board)
        sudoku_2 = sudoku_1.transpose()
        s1 = sudoku_1[0:3, :].transpose()
        s2 = sudoku_1[3:6, :].transpose()
        s3 = sudoku_1[6:9, :].transpose()
        sudoku_3 = []
        sudoku_3.append(s1[0:3,:].reshape(1, 9)[0])
        sudoku_3.append(s1[3:6,:].reshape(1, 9)[0])
        sudoku_3.append(s1[6:9,:].reshape(1, 9)[0])
        sudoku_3.append(s2[0:3,:].reshape(1, 9)[0])
        sudoku_3.append(s2[3:6,:].reshape(1, 9)[0])
        sudoku_3.append(s2[6:9,:].reshape(1, 9)[0])
        sudoku_3.append(s3[0:3,:].reshape(1, 9)[0])
        sudoku_3.append(s3[3:6,:].reshape(1, 9)[0])
        sudoku_3.append(s3[6:9,:].reshape(1, 9)[0])
        for i in range(9):
            if not self.isValid(sudoku_1[i]):
                return False
            if not self.isValid(sudoku_2[i]):
                return False
            if not self.isValid(sudoku_3[i]):
                return False
        return True

    def isValid(self, lst):
        lst = np.delete(lst, np.where(lst == '.'))
        if len(lst) == len(set(lst)):
            return True
        return False



if __name__ == '__main__':
    '''
    [[".",".","4", ".",".",".", "6","3","."],
     [".",".",".", ".",".",".", ".",".","."],
     ["5",".",".", ".",".",".", ".","9","."],
     
     [".",".",".", "5","6",".", ".",".","."],
     ["4",".","3", ".",".",".", ".",".","1"],
     [".",".",".", "7",".",".", ".",".","."],
     
     [".",".",".", "5",".",".", ".",".","."],
     [".",".",".", ".",".",".", ".",".","."],
     [".",".",".", ".",".",".", ".",".","."]]'''
    s = Solution()
    a = [[".",".","4",".",".",".","6","3","."],
     [".",".",".",".",".",".",".",".","."],
     ["5",".",".",".",".",".",".","9","."],
     [".",".",".","5","6",".",".",".","."],
     ["4",".","3",".",".",".",".",".","1"],
     [".",".",".","7",".",".",".",".","."],
     [".",".",".","5",".",".",".",".","."],
     [".",".",".",".",".",".",".",".","."],
     [".",".",".",".",".",".",".",".","."]]
    r = s.isValidSudoku(a)
    pass