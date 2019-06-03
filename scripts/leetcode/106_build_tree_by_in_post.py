#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""
"""
根据一棵树的中序遍历与后序遍历构造二叉树。

注意:
你可以假设树中没有重复的元素。

例如，给出
    中序遍历 inorder = [9,3,15,20,7]
    后序遍历 postorder = [9,15,7,20,3]
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
    def buildTree(self, inorder, postorder):
        if len(postorder) == 0:
            return None
        root = TreeNode(postorder[-1])
        idx = inorder.index(root.val)
        left_in = inorder[:idx]
        right_in = inorder[idx+1:]
        left_post = postorder[:len(left_in)]
        right_post = postorder[len(left_in):len(postorder)-1]
        root.left = self.buildTree(left_in, left_post)
        root.right = self.buildTree(right_in, right_post)
        return root


if __name__ == '__main__':
    from IPython import embed
    inorder = [9,3,15,20,7]
    postorder = [9,15,7,20,3]
    s = Solution()
    r = s.buildTree(inorder, postorder)
    embed()
    print(r)
    pass
