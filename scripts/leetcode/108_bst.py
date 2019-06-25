#!usr/bin/env python  
# -*- coding:utf-8 _*-
"""
将一个按照升序排列的有序数组，转换为一棵高度平衡二叉搜索树。

本题中，一个高度平衡二叉树是指一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过 1。

示例:

    给定有序数组: [-10,-3,0,5,9],

    一个可能的答案是：[0,-3,9,-10,null,5]，它可以表示下面这个高度平衡二叉搜索树：

              0
             / \
           -3   9
           /   /
         -10  5
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def __init__(self):
        self.root = None

    def sortedArrayToBST(self, nums):
        """
        :type nums: List[int]
        :rtype: TreeNode
        """
        self.root = None
        for num in nums:
            self.insert(self.root, None, num)
            embed()
        return self.root

    def insert(self, root, parent, num):
        if root is None:
            root = TreeNode(num)
            if parent is not None:
                if num < parent.val:
                    parent.left = root
                elif num > parent.val:
                    parent.right = root
        if num < root.val:
            self.insert(root.left, root, num)
        elif num > root.val:
            self.insert(root.right, root, num)


if __name__ == '__main__':
    from IPython import embed
    s = Solution()
    p = [-10,-3,0,5,9]
    r = s.sortedArrayToBST(p)
    embed()
    print(r)
