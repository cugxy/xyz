# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       103_zigzag_level_order.py
   Description :
   Author :          cugxy
   date：            2019/5/31
-------------------------------------------------
   Change Activity:
                     2019/5/31
-------------------------------------------------
"""
"""
给定一个二叉树，返回其节点值的锯齿形层次遍历。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

例如：
给定二叉树 [3,9,20,null,null,15,7],

        3
       / \
      9  20
        /  \
       15   7
返回锯齿形层次遍历如下：

    [
      [3],
      [20,9],
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
    def zigzagLevelOrder(self, root):
        rs = []
        if root is None:
            return rs
        q = []
        q.append(root)
        d = 0
        while len(q) != 0:
            p = []
            for i in range(len(q)):
                node = q.pop(0)
                p.append(node.val)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            if d % 2 != 0:
                p = p[::-1]
            rs.append(p)
            d += 1
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
    r = s.zigzagLevelOrder(n3)
    print(r)
    pass
