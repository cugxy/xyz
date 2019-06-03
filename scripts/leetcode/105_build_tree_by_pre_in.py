#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""
"""
根据一棵树的前序遍历与中序遍历构造二叉树。

注意:
你可以假设树中没有重复的元素。

例如，给出
    前序遍历 preorder = [3,9,20,15,7]
    中序遍历 inorder = [9,3,15,20,7]
返回如下的二叉树：

            3
           / \
          9  20
            /  \
           15   7
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def buildTree(self, preorder, inorder):
        if len(preorder) == 0:
            return None
        root = TreeNode(preorder[0])
        idx = inorder.index(root.val)
        left_in = inorder[:idx]
        right_in = inorder[idx+1:]
        left_pre = preorder[1:len(left_in)+1]
        right_pre = preorder[len(left_in)+1:]
        root.left = self.buildTree(left_pre, left_in)
        root.right = self.buildTree(right_pre, right_in)
        return root


if __name__ == '__main__':
    from IPython import embed
    preorder = [3,9,20,15,7]
    inorder = [9,3,15,20,7]
    s = Solution()
    r = s.buildTree(preorder, inorder)
    embed()
    print(r)
    pass
