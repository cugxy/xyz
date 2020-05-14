# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       111.py
   Description :
   Author :          cugxy
   date：            2019/10/31
-------------------------------------------------
   Change Activity:
                     2019/10/31
-------------------------------------------------

给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

说明: 叶子节点是指没有子节点的节点。

示例:

给定二叉树 [3,9,20,null,null,15,7],

    3
   / \
  9  20
 /  /  \
10 15   7
返回它的最小深度  2.

思路: 层次遍历, 并记录层级, 过程中 找到左右子树均为空的 节点, 则跳出, 并返回当前层级即可

"""
import queue


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        q = queue.Queue()
        c_l = 1
        n_l = 0
        level = 1
        q.put(root)
        while not q.empty():
            c_n = q.get()
            c_l -= 1
            if c_n.left:
                q.put(c_n.left)
                n_l += 1
            if c_n.right:
                q.put(c_n.right)
                n_l += 1
            if not c_n.left and not c_n.right:
                break
            if 0 == c_l:
                c_l = n_l
                n_l = 0
                level += 1
        return level


if __name__ == '__main__':
    if 1:
        n1 = TreeNode(1)
        n9 = TreeNode(9)
        n20 = TreeNode(20)
        n15 = TreeNode(15)
        n7 = TreeNode(7)
        n10 = TreeNode(10)
        n1.left = n9
        n1.right = n20
        # n9.left = n10
        n20.left = n15
        n20.right = n7
        s = Solution()
        r = s.minDepth(n1)
        print(r)
        pass
    pass

