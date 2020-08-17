# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dfs.py
   Description :
   Author :       cugxy
   date：          2018/11/26 0019
-------------------------------------------------
   Change Activity:
                   2019/5/19 0019:
-------------------------------------------------
给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。

前缀: 除了最后一个字符以外, 一个字符串的全部头部组合
后缀: 除了第一个字符意外, 一个字符串的全部尾部组合
如:
字符串:'bread'
前缀: '', 'b', 'br', 'bre', 'brea'
后缀: '', 'read', 'ead', 'ad', 'd'

部分匹配值 即 前缀 和 后缀 的最长的共有元素长度, 以 'ABCDABD' 为例
- 'A' 前缀后缀均为 空, 部分匹配值为 0
- 'AB' 前缀 [A] 后缀 [B] 共有元素长度为 0, 部分匹配值为0
- 'ABC' 的前缀为[A, AB]，后缀为[BC, C]，共有元素的长度0
- 'ABCD' 的前缀为[A, AB, ABC]，后缀为[BCD, CD, D]，共有元素的长度为0；
- 'ABCDA' 的前缀为[A, AB, ABC, ABCD]，后缀为[BCDA, CDA, DA, A]，共有元素为"A"，长度为1；
- 'ABCDAB' 的前缀为[A, AB, ABC, ABCD, ABCDA]，后缀为[BCDAB, CDAB, DAB, AB, B]，共有元素为"AB"，长度为2；
- 'ABCDABD' 的前缀为[A, AB, ABC, ABCD, ABCDA, ABCDAB]，后缀为[BCDABD, CDABD, DABD, ABD, BD, D]，共有元素的长度为0。

则匹配时 移动位数 = 已匹配字符数 - 对应的部分匹配值

"""


def KPM(haystack, needle):
    """
    Knuth-Morris-Pratt KPM 算法实现 strStr()
    :param haystack
    :param needle
    :return int 0 包含 -1 不包含
    """
    def partial_match_value(_s):
        """
        计算部分匹配值
        :param _s:
        :return:
        """
        if not _s:
            return 0
        l = len(_s)
        for i in range(1, l):
            prefix = _s[:l - i]
            suffix = _s[i:]
            if prefix == suffix:
                return l - i
        return 0

    def partial_match_table(_s):
        """
        计算部分匹配表
        :param _s:
        :return:
        """
        if not _s:
            return []
        l = len(_s)
        result = []
        for i in range(1, l + 1):
            v = partial_match_value(_s[:i])
            result.append(v)
        return result

    if haystack is None:
        return -1
    if needle is None or len(needle) == 0:
        return 0
    l_h = len(haystack)
    l_n = len(needle)
    if l_n == l_h:
        if haystack == needle:
            return 0
        return -1
    if haystack is None or l_h < l_n:
        return -1
    if needle is None or l_n == 0:
        return 0
    _partial_match_table = partial_match_table(needle)
    i = 0
    while l_h - i >= l_n:                                           # 长串遍历
        if haystack[i] == needle[0]:                                # 如果当前字符串相等
            k = 1
            found = True
            for k in range(1, l_n):                                 # 遍历子串
                if i + k >= l_h or haystack[i + k] != needle[k]:    # 如果元素不相等
                    found = False                                   # 设置 found flag
                    break
            if found:                                               # found flag 为 True 则表示找到了
                return i
            i = i + k - _partial_match_table[k - 1]                 # 根据 部分匹配表 移动长串遍历 index
        else:
            i = i + 1                                               # 当前字符串不相等, 移动 index + 1
    return -1
