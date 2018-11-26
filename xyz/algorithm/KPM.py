#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy   
@file:  KPM.py
@time:  2018-11-26
"""

def KPM(haystack, needle):
    """
    KPM 算法实现 strStr()
    :param haystack 
    :param needle
    :return int
    """
    def partial_match_value(_s):
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
        if not _s:
            return []
        l = len(_s)
        result = []
        for i in range(1, l + 1):
            v = partial_match_value(_s[:i])
            result.append(v)
        return result
    
    l_h = len(haystack)
    l_n = len(needle)
    if l_n == l_h:
        if haystack == needle:
            return 0
        else:
            return -1
    if haystack is None or l_h < l_n:
        return -1
    if needle is None or l_n == 0:
        return 0
    _partial_match_table = partial_match_table(needle)
    i = 0
    while(l_h - i >= l_n):
        if haystack[i] == needle[0]:
            k = 1
            found = True
            for k in range(1, l_n):
                if i + k >= l_h or haystack[i + k] != needle[k]:
                    found = False
                    break
            if found:
                return i
            i = i + k - _partial_match_table[k - 1]
        else:
            i = i + 1
    return -1


if __name__ == '__main__':
    r = KPM('asdf', 'df')
    print(r)