#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        lst = []
        node = head
        while node:
            lst.append(node)
            node = node.next
        l = len(lst)
        n = l - n
        if n - 1 < 0:
            return head.next
        if n + 1 == l:
            lst[n - 1].next = None
        elif n + 1 > l:
            pass
        else:
            lst[n - 1].next = lst[n + 1]
        return head


if __name__ == '__main__':
    node_0 = ListNode(0)
    node_1 = ListNode(1)
    node_2 = ListNode(2)
    node_3 = ListNode(3)
    node_4 = ListNode(4)
    node_5 = ListNode(5)
    node_0.next = node_1
    node_1.next = node_2
    node_2.next = node_3
    node_3.next = node_4
    node_4.next = node_5

    s = Solution()
    r = s.removeNthFromEnd(node_0, 2)
    pass