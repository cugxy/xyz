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
    """
    给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。

    请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。

    你可以假设 nums1 和 nums2 不会同时为空。

    示例 1:

    nums1 = [1, 3]
    nums2 = [2]

    则中位数是 2.0
    示例 2:

    nums1 = [1, 2]
    nums2 = [3, 4]

    则中位数是 (2 + 3)/2 = 2.5
    """
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