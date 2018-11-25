#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:$USER
@file: $NAME 
@time: $YEAR/$MONTH/$DAY
"""  
def swap(lst, i, j):
    tmp = lst[i]
    lst[i] = lst[j]
    lst[j] = tmp


def bubble_sort(lst, compare_fun):
    """
    冒泡排序 O(n^2) O(n^2) O(n)
    """
    if not lst:
        return []
    l = len(lst)
    for i in range(l):
        for j in range(i + 1, l):
            if compare_fun(lst[i], lst[j]) > 0:
                swap(lst, i, j)


def select_sort(lst, compare_fun):
    """
    选择排序，选取最小的 O(n^2) O(n^2) O(n^2)
    """
    if not lst:
        return []
    l = len(lst)
    for i in range(l):
        m_idx = i
        for j in range(i + 1, l):
            if compare_fun(lst[j], lst[m_idx]) < 0:
                m_idx = j
        swap(lst, i, m_idx)


def insert_sort(lst, compare_fun):
    """
    插入排序，
    """
    if not lst:
        return []
    l = len(lst)
    for i in range(l):
        p_idx = i - 1
        val = lst[i]
        while p_idx >= 0 and compare_fun(lst[p_idx], val) > 0:
            lst[p_idx + 1] = lst[p_idx]
            p_idx -= 1
        lst[p_idx+ 1] = val
 

def shell_sort(lst):
    pass


if __name__ == '__main__':
    if 1:
        lst = [1, 3]
        print(lst)
        swap(lst, 0, 1)
        print(lst)
        
