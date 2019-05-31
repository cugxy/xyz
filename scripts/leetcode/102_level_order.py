# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     102_level_order.py
   Description :
   Author :       cugxy
   date：         2019/05/30
-------------------------------------------------
   Change Activity:
                  2019/05/30
-------------------------------------------------
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
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def levelOrder(self, root: TreeNode):
        rs = []
        if root is None:
            return rs
        q = []
        q.append(root)
        while len(q) != 0:
            p = []
            for i in range(len(q)):
                node = q.pop(0)
                p.append(node.val)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            rs.append(p)
        return rs


if __name__ == '__main__':
    n3 = TreeNode(3)
    n9 = TreeNode(9)
    n20 = TreeNode(20)
    n15 = TreeNode(15)
    n7 = TreeNode(7)
    n3.left = n9
    n3.right = n20
    n20.left = n15
    n20.right = n7
    s = Solution()
    r = s.levelOrder(n3)
    print(r)

