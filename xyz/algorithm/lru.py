# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     lru.py
   Description :
   Author :       cugxy
   date：          2019/7/23 0019
-------------------------------------------------
   Change Activity:
                   2019/7/23 0019:
-------------------------------------------------
"""


class ListNode(object):
    """
    双向链表
    """
    def __init__(self, key=None, val=None):
        self.key = key
        self.val = val
        self.pre = None
        self.next = None

    def __repr__(self):
        return 'ListNode key: %s | val: %s' % (self.key, self.val, )


class LRUCache(object):
    """
    利用双向链表实现 LRU, 定义 头尾两个节点, 其他数据均记录在头尾两个节点中, 并使用 字典实现 O(1) 查找
    """
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.count = 0
        self.cap = capacity
        self.data = {}              # key <-> ListNode
        self.head = ListNode('head', 'head')
        self.tail = ListNode('tail', 'tail')
        self.head.next = self.tail
        self.tail.pre = self.head

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        node = self.data.get(key, None)
        if not node:
            return -1
        self._move_to_head(node)
        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        node = self.data.get(key, None)
        if node:
            node.val = value
            self._move_to_head(node)
            return
        node = ListNode(key, value)
        self.data[key] = node
        self._add(node)
        self.count += 1
        if self.count > self.cap:
            tail = self._pop_node()
            self.data.pop(tail.key)
            self.count -= 1

    def _add(self, node):
        node.pre = self.head
        node.next = self.head.next
        self.head.next.pre = node
        self.head.next = node

    def _remove(self, node):
        pre = node.pre
        _next = node.next
        pre.next = _next
        _next.pre = pre

    def _move_to_head(self, node):
        self._remove(node)
        self._add(node)

    def _pop_node(self):
        res = self.tail.pre
        self._remove(res)
        return res
