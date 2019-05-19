#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:cugxy 
@file: 95generateTrees.py 
@time: 2019/03/19 
"""

"""
给定一个整数 n，生成所有由 1 ... n 为节点所组成的二叉搜索树。

示例:

输入: 3
输出:
[
  [1,null,3,2],
  [3,2,null,1],
  [3,1,null,null,2],
  [2,1,3],
  [1,null,2,null,3]
]
解释:
以上的输出对应以下 5 种不同结构的二叉搜索树：

   1         3     3      2      1
    \       /     /      / \      \
     3     2     1      1   3      2
    /     /       \                 \
   2     1         2                 3
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __str__(self):
        return 'val:%i left:%s right:%s' % (self.val, self.left, self.right, )


class Solution(object):
    def generateTrees(self, n):
        """
        类似第 96 题,当 n <= 1 时, 直接返回 [Node(n), ]
        当 n > 1 时, 则对于 i(遍历 n), 二叉树, 为 lefts i rights (中序遍历), 其中 lefts 为 左子树可能的列表, rights 为右子树可能列表
        :type n: int
        :rtype: List[TreeNode]
        """
        if n < 1:
            return []
        return self.fun(1, n)

    def fun(self, s, e):
        result = []
        if s > e:
            result.append(None);
            return result
        for i in range(s, e + 1):
            lefts = self.fun(s, i - 1)
            rights = self.fun(i + 1, e)
            for left in lefts:
                for right in rights:
                    root = TreeNode(i)
                    root.left = left
                    root.right = right
                    result.append(root)
        return result


if __name__ == '__main__':
    s = Solution()
    r = s.generateTrees(3)
    print(r)
    pass