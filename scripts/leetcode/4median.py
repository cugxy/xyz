#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


def sort(l1, l2):
    i = 0
    j = 0
    r = []
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            r.append(l1[i])
            i += 1
        else:
            r.append(l2[j])
            j += 1
    while i < len(l1):
        r.append(l1[i])
        i += 1
    while j < len(l2):
        r.append(l2[j])
        j += 1
    return r




class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        l = sort(nums1, nums2)
        y = len(l) % 2
        m = int(len(l) / 2)
        if y is not 0:
            return l[m]
        else:
            return (l[m-1] + l[m])/2


if __name__ == '__main__':
    s = Solution()
    r = s.findMedianSortedArrays([1], [2, 3])
    pass