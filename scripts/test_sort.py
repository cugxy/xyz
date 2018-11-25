#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:$USER
@file: $NAME 
@time: $YEAR/$MONTH/$DAY
"""  

if __name__ == '__main__':
    if 1:
        from xyz.algorithm.sort import *
        a = [1, 43, 2389, 290, 28, 19, 984, 38, 2, 239, 90, 43, ]
        def compare_lst(m, n):
            if m < n:
                return -1
            elif m == n:
                return 0
            else:
                return 1
        print(a)
        select_sort(a, compare_lst)
        print(a)