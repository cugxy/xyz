#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:cugxy
@file: 102levelOrder
@time: 2019/1/31
"""
"""
给定一个二叉树，返回其按层次遍历的节点值。 （即逐层地，从左到右访问所有节点）。

例如:
给定二叉树: [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回其层次遍历结果：

[
  [3],
  [9,20],
  [15,7]
]
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        result = []
        if not root:
            return result
        tmp_lst1 = []
        tmp_lst2 = []
        tmp_lst1.append(root)
        while tmp_lst1:
            node = tmp_lst1.pop()









if __name__ == '__main__':
    pass