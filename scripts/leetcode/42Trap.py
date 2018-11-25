class Solution:
    """
    给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
    输入: [0,1,0,2,1,0,1,3,2,1,2,1]
    输出: 6
    """
    def trap(self, height):
        """
        穷举 超出时间限制  m * n
        :type height: List[int]
        :rtype: int
        """
        if not height:
            return 0
        max_h = max(height)
        min_h = min(height)
        height = [_ - min_h for _ in height]
        trap_sum = 0
        for i in range(max_h - min_h):
            num, r, l = 0, 0, 0
            for _r in range(len(height)):
                if height[_r] > i:  # 找到右边 
                    r = _r
                    break
            for _l in range(len(height)):
                if height[len(height) - _l - 1] > i: # 左边
                    l = len(height) - _l - 1
                    break
            for _ in range(r + 1, l):
                if height[_] <= i:
                    num += 1
            if num > 0:
                trap_sum += num
        return trap_sum

    def trap2(self, height):
        """
        分治算法，找出最高点，分左右而治之
        时间 O(n) 总体来说 只遍历了 n 次
        空间 O(1)
        """
        if not height:
            return 0
        if len(height) == 1:
            return 0
        if len(height) == 2:
            return 0
        idx, h = 0, 0
        for _ in range(len(height)):
            if height[_] > h:           # 找到左边第一个局部最高点
                idx = _
                h = height[idx]
        if idx == 0:
            sum = 0
            h1, h2 = height[len(height) - 1], 0
            for j in range(len(height) - 1, 1, -1):
                h2 = height[j]
                if h2 < h1:
                    sum += (h1 - h2)
                else:
                    h1 = h2
            return sum
        if idx == len(height) - 1:
            sum = 0
            h1, h2 = height[0], 0
            for k in range(1, len(height) - 1):
                h2 = height[k]
                if h2 < h1:
                    sum += (h1 - h2)
                else:
                    h1 = h2
            return sum
        left = height[0:idx + 1]
        right = height[idx: len(height)]
        num_l = self.trap2(left)
        num_r = self.trap2(right)
        return num_l + num_r

if __name__ == '__main__':
    s = Solution()
    r = s.trap2([0,1,0,2,1,0,1,3,2,1,2,1])
    print(r)
    pass
