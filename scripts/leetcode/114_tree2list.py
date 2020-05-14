# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       114_tree2list.py
   Description :
   Author :          cugxy
   date：            2019/10/30
-------------------------------------------------
   Change Activity:
                     2019/10/30
-------------------------------------------------

给定一个二叉树，原地将它展开为链表。

例如，给定二叉树

    1
   / \
  2   5
 / \   \
3   4   6
将其展开为：

1
 \
  2
   \
    3
     \
      4
       \
        5
         \
          6

"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.rs = []

    def flatten(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        self.preview(root)
        if len(self.rs) <= 1:
            return
        t = TreeNode(self.rs[1])
        root.left = None
        root.right = t
        for idx, e in enumerate(self.rs):
            if idx <= 1:
                continue
            temp = TreeNode(e)
            t.right = temp
            t = temp

    def preview(self, root):
        if root:
            self.rs.append(root.val)
            self.preview(root.left)
            self.preview(root.right)


if __name__ == '__main__':
    if 1:
        n1 = TreeNode(1)
        n2 = TreeNode(2)
        n3 = TreeNode(3)
        n4 = TreeNode(4)
        n5 = TreeNode(5)
        n6 = TreeNode(6)
        n1.left = n2
        n1.right = n5
        n2.left = n3
        n2.right = n4
        n5.right = n6
        s = Solution()
        s.flatten(n1)
        print(n1)
    pass

