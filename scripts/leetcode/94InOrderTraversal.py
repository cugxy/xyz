#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    result = []

    def inorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        self.result = []
        if root == []:
            return self.result
        self.func(root)
        return self.result

    def func(self, root):
        if root is None:
            return
        if root.left is not None:
            self.func(root.left)
        if root is not None:
            self.result.append(root.val)
        if root.right is not None:
            self.func(root.right)


if __name__ == '__main__':
    root = TreeNode()
    s = Solution()
    r = s.inorderTraversal([])
    pass