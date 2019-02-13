#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:cugxy 
@file: 53MaxSubArray.py.py 
@time: 2019/02/13 
"""
import sys


class Solution:
    """
    给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
    示例:
    输入: [-2,1,-3,4,-1,2,1,-5,4],
    输出: 6
    解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
    进阶:
    如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。
    """
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        result = -sys.maxsize
        ant = 0
        for i in range(len(nums)):
            if ant < 0: ant = 0
            ant += nums[i]
            result = max(ant, result)
        return result


if __name__ == '__main__':
    s = Solution()
    r = s.maxSubArray([-2,1,-3,4,-1,2,1,-5,4])
    print(r)