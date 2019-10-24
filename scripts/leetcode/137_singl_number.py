#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:cugxy 
@file: 137_singl_number.py.py 
@time: 2019/10/24

给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现了三次。找出那个只出现了一次的元素。

说明：

你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？

示例 1:

输入: [2,2,3,2]
输出: 3
示例 2:

输入: [0,1,0,1,0,1,99]
输出: 99

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/single-number-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


class Solution:
    """
    """
    def singleNumber(self, nums: list) -> int:
        s = set(nums)
        sum1 = sum(s)
        sum2 = sum(nums)
        return int((sum1 * 3 - sum2) / 2)


if __name__ == '__main__':
    if 1:
        param = [0, 1, 0, 1, 0, 1, 99]
        s = Solution()
        r = s.singleNumber(param)
        print(r)
    pass

