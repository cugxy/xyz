#!usr/bin/env python  
# -*- coding:utf-8 _*-
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
        return False
    l = len(lst)
    for i in range(l):
        for j in range(i + 1, l):
            if compare_fun(lst[i], lst[j]) > 0:
                swap(lst, i, j)
    return True


def select_sort(lst, compare_fun):
    """
    选择排序，选取最小的 O(n^2) O(n^2) O(n^2)
    """
    if not lst:
        return False
    l = len(lst)
    for i in range(l):
        m_idx = i
        for j in range(i + 1, l):
            if compare_fun(lst[j], lst[m_idx]) < 0:
                m_idx = j
        swap(lst, i, m_idx)
    return True


def insert_sort(lst, compare_fun):
    """
    插入排序，
    """
    if not lst:
        return False
    l = len(lst)
    for i in range(l):
        p_idx = i - 1
        val = lst[i]
        while p_idx >= 0 and compare_fun(lst[p_idx], val) > 0:
            lst[p_idx + 1] = lst[p_idx]
            p_idx -= 1
        lst[p_idx+ 1] = val
    return True
 

def shell_sort(lst):
    pass


def quick_sort(lst, r, l, compare_fun):
    if not lst or not r or not l or not compare_fun:
        return False
    if l < r:
        return False

    def partition(lst, l, r):
        x = lst[r]
        i = l - 1
        for j in range(l, r):
            if compare_fun(lst[j], x) <= 0:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[i + 1], lst[r] = lst[r], lst[i+1]
        return i + 1

    def _quick_sort(lst, l, r):
        if l < r:
            q = partition(lst, l, r)
            _quick_sort(lst, l, q - 1)
            _quick_sort(lst, q + 1, r)
    _quick_sort(lst, r, l)
    return True


if __name__ == '__main__':
    if 1:
        lst = [1, 3]
        print(lst)
        swap(lst, 0, 1)
        print(lst)

