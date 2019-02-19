#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: sudoku.py
@time: 2019/2/19
"""


class Sudoku:
    """
    数独
    """
    N = 9
    ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, ]

    def __init__(self, board):
        self.board = board

    def check(self):
        pass

    def calculate(self):
        self.__first_insert()

        pass

    def check_ok(self):
        pass

    def print(self):
        print(self.board)

    def __first_insert(self):
        """
        第一次计算，确定可以确定的值
        :return:
        """
        while True:
            flag = True
            for i in range(self.N):
                for j in range(self.N):
                    if self.board[i][j] != 0:
                        continue
                    r = self.__calculate_in_i_j(i, j)
                    if len(r) != 1:
                        continue
                    self.board[i][j] = r[0]
                    flag = False
            if flag:
                break

    def __calculate_in_i_j(self, i, j):
        """
        计算 i j 位置的可能值
        :param i:
        :param j:
        :return:
        """
        row = self.board[i]
        col = [x[j] for x in self.board]
        sq = []
        i = int(i / 3) * 3
        j = int(j / 3) * 3
        for _i in range(3):
            for _j in range(3):
                sq.append(self.board[i + _i][j + _j])
        sq.extend(row)
        sq.extend(col)
        sq = list(set(sq))
        return [x for x in self.ALL if x not in sq]


if __name__ == '__main__':
    s = [[8, 1, 0, 7, 3, 0, 0, 2, 9, ],
         [5, 6, 0, 0, 4, 1, 0, 0, 0, ],
         [0, 0, 0, 8, 0, 0, 0, 0, 0, ],
         [6, 4, 5, 0, 7, 0, 0, 9, 0, ],
         [0, 3, 8, 0, 0, 9, 0, 0, 7, ],
         [7, 0, 2, 6, 0, 3, 0, 1, 4, ],
         [4, 5, 0, 3, 1, 2, 9, 8, 6, ],
         [0, 0, 1, 5, 6, 0, 4, 0, 2, ],
         [3, 2, 6, 9, 8, 4, 7, 5, 0, ],
         ]
    sudoku = Sudoku(s)
    sudoku.calculate()
    sudoku.print()

    pass