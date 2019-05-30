#!usr/bin/env python  
# -*- coding:utf-8 _*-
"""
给定两个二叉树，编写一个函数来检验它们是否相同。

如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。

示例 1:
    输入:      1         1
              / \       / \
             2   3     2   3

            [1,2,3],   [1,2,3]

    输出: true

示例 2:
    输入:      1          1
              /           \
             2             2

            [1,2],     [1,null,2]

    输出: false

示例 3:
    输入:
               1         1
              / \       / \
             2   1     1   2

            [1,2,1],   [1,1,2]

    输出: false
"""
import operator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        pre_p = []
        pre_q = []
        mid_p = []
        mid_q = []
        self._pre(p, pre_p)
        self._pre(q, pre_q)
        self._mid(p, mid_p)
        self._mid(q, mid_q)
        return operator.eq(pre_p, pre_q) and operator.eq(mid_p, mid_q)

    def _pre(self, root, rs):
        if root is None:
            rs.append('null')
            return
        rs.append(root.val)
        self._pre(root.left, rs)
        self._pre(root.right, rs)
    
    def _mid(self, root, rs):
        if root is None:
            rs.append('null')
            return
        self._pre(root.left, rs)
        rs.append(root.val)
        self._pre(root.right, rs)
    

if __name__ == '__main__':
    s = Solution()
    
