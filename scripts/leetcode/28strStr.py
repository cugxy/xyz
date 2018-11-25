#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


class Solution:
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """
        l_h = len(haystack)
        l_n = len(needle)
        if haystack is None or l_h < l_n:
            return -1
        if needle is None or l_n == 0:
            return 0
        index = []
        for i in range(l_h):
            if haystack[i] == needle[0] and l_h - i > l_n - 1:
                index.append(i)
        if index is []:
            return -1
        for j in index:
            k = 1
            found = True
            for k in range(1, l_n):
                if j + k >= l_h or haystack[j + k] != needle[k]:
                    found = False
                    break
            if found:
                return j
        return -1


class KPMSolution:
    def strStr(self, haystack, needle):
        """
        KPM 实现 strStr
        :param haystack:
        :param needle:
        :return:
        """
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
        partial_match_table = self.get_partial_match_table(needle)
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
                i = i + k - partial_match_table[k - 1]
            else:
                i = i + 1
        return -1

    def get_partial_match_table(self, needle):
        l = len(needle)
        result = []
        for i in range(1, l + 1):
            v = self.get_partial_match_value(needle[:i])
            result.append(v)
        return result

    def get_partial_match_value(self, subStr):
        l = len(subStr)
        for i in range(1, l):
            prefix = subStr[:l - i]
            suffix = subStr[i:]
            if prefix == suffix:
                return l - i
        return 0


if __name__ == '__main__':
    s = KPMSolution()
    st = "BBC ABCDAB ABCDABCDABDE"
    p = "ABCDABD"
    st = "mississippi"
    p = "pi"
    r = s.strStr(st, p)
    pass