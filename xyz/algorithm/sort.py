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
    if i == j:
        return
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
            if compare_fun(lst[m_idx], lst[j]) > 0:
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
    for i in range(1, l):
        p_idx = i - 1
        val = lst[i]
        while p_idx >= 0 and compare_fun(lst[p_idx], val) > 0:
            lst[p_idx + 1] = lst[p_idx]
            p_idx -= 1
        lst[p_idx + 1] = val
    return True


def shell_sort(lst, compare_fun):
    """
    希尔排序
    """
    if not lst:
        return False
    l = len(lst)
    step = l // 2                   # 步长
    while step > 0:
        for i in range(step, l):        # 跳一个 step 的插入排序
            val = lst[i]
            j = i
            while j >= 0 and j - step >= 0 and compare_fun(lst[j - step], val) > 0:
                lst[j] = lst[j - step]
                j -= step
            lst[j] = val
        step = step // 2
    return True


def quick_sort(lst, r, l, compare_fun):
    """
    快速排序
    :param lst:
    :param r:
    :param l:
    :param compare_fun:
    :return:
    """
    if not lst or not compare_fun:
        return False
    if l < r:
        return False

    def _partition(lst, l, r):
        x = lst[l]                              # 基准数
        idx = l + 1                             # 遍历 index
        i = idx
        while i <= r:                           # 确定基准应当放置的位置
            if compare_fun(x, lst[i]) > 0:
                swap(lst, i, idx)               # 将大数向后移动
                idx += 1                        # 定位 基准数应当放置的位置
            i += 1
        swap(lst, l, idx - 1)                   # 移动基准数到指定位置, 此时 基准数左边都小于基准数, 右边均大于基准数
        return idx - 1                          # 返回基准数位置

    def _quick_sort(lst, l, r):
        if l < r:
            q = _partition(lst, l, r)
            _quick_sort(lst, l, q - 1)
            _quick_sort(lst, q + 1, r)
    _quick_sort(lst, r, l)
    return True
