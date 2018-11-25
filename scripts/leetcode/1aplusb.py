#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time:  
"""

class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        i = 0
        for i in range(len(nums)):
            a = nums[i]
            i += 1
            for _ in range(i, len(nums)):
                b = nums[_]
                if a + b == target:
                    return [i - 1, _]



if __name__ == '__main__':
    s = Solution()
    r = s.twoSum([2, 7, 11, 15], 9)
    pass