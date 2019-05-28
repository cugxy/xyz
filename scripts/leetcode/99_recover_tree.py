#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
二叉搜索树中的两个节点被错误地交换。请在不改变其结构的情况下，恢复这棵树。

示例 1:
    输入: [1,3,null,null,2]

       1
      /
     3
      \
       2

    输出: [3,1,null,null,2]

       3
      /
     1
      \
       2
示例 2:
    输入: [3,1,4,null,null,2]

      3
     / \
    1   4
       /
      2

    输出: [2,1,4,null,null,3]

      2
     / \
    1   4
       /
      3
进阶:
    使用 O(n) 空间复杂度的解法很容易实现。
    你能想出一个只使用常数空间的解决方案吗？
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def recoverTree(self, root):
        """
        :type root: TreeNode
        :rtype: None Do not return anything, modify root in-place instead.
        """
        rs = []
        self._order(root, rs)
        srs = rs.copy()
        srs.sort()
        val1, val2 = None, None
        for i in range(len(srs)):
            if srs[i] == rs[i]:
                continue
            val1 = srs[i]
            val2 = rs[i]
            break
        node1 = self._find(root, val1)
        node2 = self._find(root, val2)
        node1.val = val2
        node2.val = val1
        embed()
        return root

    def _order(self, root, rs):
        if root is None:
            return
        self._order(root.left, rs)
        rs.append(root.val)
        self._order(root.right, rs)
    
    def _find(self, root, val):
        if root is None:
            return None
        if root.val == val:
            return root
        node = self._find(root.left, val)
        if node is not None:
            return node
        node = self._find(root.right, val)
        if node is not None:
            return node
        return node


if __name__ == '__main__':
    from IPython import embed
    n1 = TreeNode(1)       
    n2 = TreeNode(2)
    n3 = TreeNode(3)
    n4 = TreeNode(4)
    n5 = TreeNode(5)
    n6 = TreeNode(6)

    s = Solution()

    if 1:
        n1.left = n3
        n3.right = n2
        s.recoverTree(n1)
    if 0:
#      3
#     / \
#    1   4
#       /
#      2
        n3.left = n1
        n3.right = n4
        n4.left = n2
        s.recoverTree(n3)

    embed()






