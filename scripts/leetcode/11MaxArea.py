#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""


class Solution:
    """
    给定 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，
    垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0)。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。
    说明：你不能倾斜容器，且 n 的值至少为 2。
    示例:

    输入: [1,8,6,2,5,4,8,3,7]
    输出: 49
    """
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