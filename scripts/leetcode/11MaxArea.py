#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""

from IPython import embed


class Solution:
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        count = len(height)
        left_idx = 0
        right_idx = count - 1
        max_s = 0
        while left_idx < right_idx:
            left = height[left_idx]
            right = height[right_idx]
            s = min(left, right) * (right_idx - left_idx)
            if s > max_s:
                max_s = s
            if left > right:
                right_idx = right_idx - 1
            else :
                left_idx = left_idx + 1
        return max_s




if __name__ == '__main__':
    s = Solution()
    h = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    r = s.maxArea(h)
    print(r)
    pass