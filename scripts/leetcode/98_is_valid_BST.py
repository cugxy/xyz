#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: cugxy
@file:  
@time: 2019-05-19
"""


class TreeNode(object):
    """
    # Definition for a binary tree node.
    """
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    """
    给定一个二叉树，判断其是否是一个有效的二叉搜索树。

    假设一个二叉搜索树具有如下特征：

        - 节点的左子树只包含小于当前节点的数。
        - 节点的右子树只包含大于当前节点的数。
        - 所有左子树和右子树自身必须也是二叉搜索树。
    输入:
            2
           / \
          1   3
    输出: true
    输入:
            5
           / \
          1   4
             / \
            3   6
    输出: false
    解释: 输入为: [5,1,4,null,null,3,6]。
     根节点的值为 5 ，但是其右子节点值为 4 。
    """
    lst = []
    def isValidBST(self, root):
        """
        二叉树中序遍历 解决
        :type root: TreeNode
        :rtype: bool
        """
        if not root:
            return True
        self.get_list(root)
        return self.lst == sorted(list(set(self.lst)))

    def get_list(self, root):
        if not root:
            return
        if root.left is not None:
            self.get_list(root.left)
        self.lst.append(root.val)
        if root.right is not None:
            self.get_list(root.right)



if __name__ == '__main__':
    s = Solution()
    # [10,5,15,null,null,6,20]
    """
            10
           /  \
          5   15
             /  \
            6   20
    """
    n0 = TreeNode(0)
    n10 = TreeNode(10)
    n5 = TreeNode(5)
    n15 = TreeNode(15)
    n6 = TreeNode(6)
    n20 = TreeNode(20)

    n10.left = n5
    n10.right = n15
    n15.left = n6
    n15.right = n20
    r = s.isValidBST(n0)
    print(r)
