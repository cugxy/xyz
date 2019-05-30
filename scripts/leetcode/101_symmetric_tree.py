#!usr/bin/env python  
# -*- coding:utf-8 _*-
# Definition for a binary tree node.
"""
给定一个二叉树，检查它是否是镜像对称的。

例如，二叉树 [1,2,2,3,4,4,3] 是对称的。

            1
           / \
          2   2
         / \ / \
        3  4 4  3
但是下面这个 [1,2,2,null,3,null,3] 则不是镜像对称的:

            1
           / \
          2   2
           \   \
           3    3
"""


import operator
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if root is None:
            return False
        rs = []
        self._pre(root, rs, 0)
        if len(rs) % 2 == 0:
            return False
        cou = int(len(rs) / 2)
        rs1 = rs[:cou]
        rs2 = rs[cou+1:]
        rs2.reverse()
        return operator.eq(rs1, rs2)

    def _pre(self, root, rs, i):
        i += 1
        if root is None:
            return
        self._pre(root.left, rs, i)
        rs.append('%i-%i' % (root.val, i))
        self._pre(root.right, rs, i)


if __name__ == '__main__':
    from IPython import embed
    """
    [1,2,2,2,null,2]
            
            1
           / \
          2   2
         /   /
        2   2
    """

    n1 = TreeNode(1)
    n2 = TreeNode(2)
    n22 = TreeNode(2)
    n222 = TreeNode(2)
    n2222 = TreeNode(2)
    n1.left = n2
    n1.right = n22
    n2.left = n222
    n22.left = n2222
    s = Solution()
    r = s.isSymmetric(n1)


    print(r)
    pass
