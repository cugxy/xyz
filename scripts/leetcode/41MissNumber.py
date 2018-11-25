class Solution(object):
    """
    给定一个未排序的整数数组，找出其中没有出现的最小的正整数。
    """
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = [x for x in nums if x > 0]
        nums = list(set(nums))
        if not nums:
            return 1
        max_v = max(nums)
        min_v = min(nums)
        if min_v != 1:
            return 1
        flag = True
        for i in range(min_v, max_v + 1):
            if i not in nums:
                flag = False
                break
        if flag:
            return max_v + 1
        else:
            for i in range(min_v, max_v + 1):
                if i not in nums:
                    return i
        

if __name__ == '__main__':
    print(Miss([7, 8, 9, 11, 12]))
        
