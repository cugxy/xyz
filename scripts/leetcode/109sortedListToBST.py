# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       109sortedListToBST
   Description :
   Author :          cugxy
   date：            2019/7/23
-------------------------------------------------
   Change Activity:
                     2019/7/23
-------------------------------------------------
给定一个单链表，其中的元素按升序排序，将其转换为高度平衡的二叉搜索树。

本题中，一个高度平衡二叉树是指一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过 1。

示例:

给定的有序链表： [-10, -3, 0, 5, 9],

一个可能的答案是：[0, -3, 9, -10, null, 5], 它可以表示下面这个高度平衡二叉搜索树：

      0
     / \
   -3   9
   /   /
 -10  5

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/convert-sorted-list-to-binary-search-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def get_mid(head):
    pre = head
    q = head.next.next
    while q is not None and q.next is not None:
        pre = pre.next
        q = q.next.next
    return pre


class Solution(object):
    def sortedListToBST(self, head):
        """
        :type head: ListNode
        :rtype: TreeNode
        """
        if head is None:
            return None
        if head.next is None:
            return TreeNode(head.val)
        mid = get_mid(head)
        p = mid.next
        mid.next = None
        root = TreeNode(p.val)
        l_node = self.sortedListToBST(head)
        r_node = self.sortedListToBST(p.next)
        root.left = l_node
        root.right = r_node
        return root


if __name__ == '__main__':
    n_10 = ListNode(-10)
    n_3 = ListNode(-3)
    n0 = ListNode(0)
    n5 = ListNode(5)
    n9 = ListNode(9)
    n_10.next = n_3
    n_3.next = n0
    n0.next = n5
    n5.next = n9
    s = Solution()
    r = s.sortedListToBST(n_10)
    print(r)
