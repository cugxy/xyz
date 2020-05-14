# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sort.py
   Description :
   Author :       cugxy
   date：          2019/7/23 0019
-------------------------------------------------
   Change Activity:
                   2019/7/23 0019:
-------------------------------------------------
"""


def swap(lst, i, j):
    """交换"""
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
    """
    希尔排序
    :param lst:
    :return:
    """
    pass


def quick_sort(lst, r, l, compare_fun):
    """
    快速排序
    :param lst:
    :param r:
    :param l:
    :param compare_fun:
    :return:
    """
    if not lst or not r or not l or not compare_fun:
        return False
    if l < r:
        return False

    def _partition(lst, l, r):
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
            q = _partition(lst, l, r)
            _quick_sort(lst, l, q - 1)
            _quick_sort(lst, q + 1, r)
    _quick_sort(lst, r, l)
    return True
