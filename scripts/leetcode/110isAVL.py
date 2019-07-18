# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       110isAVL
   Description :
   Author :          cugxy
   date：            2019/7/18
-------------------------------------------------
   Change Activity:
                     2019/7/18
-------------------------------------------------

给定一个二叉树，判断它是否是高度平衡的二叉树。

本题中，一棵高度平衡二叉树定义为：

一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过1。

示例 1:

给定二叉树 [3,9,20,null,null,15,7]

    3
   / \
  9  20
    /  \
   15   7
返回 true 。

示例 2:

给定二叉树 [1,2,2,3,3,null,null,4,4]

       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
返回 false 。

示例 2:

给定二叉树 [1,2,2,3,3,null,null,4,4]

       1
      /
     2
    /
   3
  /
 4
返回 false 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/balanced-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """


if __name__ == '__main__':
    s = Solution()
    if 1:
        n3 = TreeNode(3)
        n9 = TreeNode(9)
        n20 = TreeNode(20)
        n15 = TreeNode(15)
        n7 = TreeNode(7)
        n3.left = n9
        n3.right = n20
        n20.left = n15
        n20.right = n7
        print(s.isBalanced(n3))
    if 1:
        n1 = TreeNode(1)
        n2 = TreeNode(2)
        n2_1 = TreeNode(2)
        n3 = TreeNode(3)
        n3_1 = TreeNode(3)
        n4 = TreeNode(4)
        n4_1 = TreeNode(4)
        n1.left = n2
        n1.right = n2_1
        n2.left = n3
        n2.right = n3_1
        n3.left = n4
        n3.right = n4_1
        print(s.isBalanced(n1))
    if 1:
        n1 = TreeNode(1)
        n2 = TreeNode(2)
        n3 = TreeNode(3)
        n1.left = n2
        n2.left = n3
        print(s.isBalanced(n1))
    pass



