# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       116.py
   Description :
   Author :          cugxy
   date：            2019/10/30
-------------------------------------------------
   Change Activity:
                     2019/10/30
-------------------------------------------------

给定一个完美二叉树，其所有叶子节点都在同一层，每个父节点都有两个子节点。二叉树定义如下：

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL。

初始状态下，所有 next 指针都被设置为 NULL。


思路: 二叉树 层次遍历, 再根据满二叉树性质划分层级, 再依次赋值

层次遍历: 借助队列实现层次遍历
- 跟节点进队列
- 队列中 pop 一个节点, 并写入结果列表保存, 同时让该节点的 孩子入队列,
- 重复上述操作

层级划分
l = log2(n) - 1
1, 2, 4, ..., 2^(l)

"""
import queue

import math


class Node:
    """
    # Definition for a Node.
    """
    def __init__(self, val, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root):
        if not root:
            return root
        lst = queue.Queue()
        crs = []
        lst.put(root)
        while not lst.empty():
            node = lst.get()
            crs.append(node)
            if node.left:
                lst.put(node.left)
            if node.right:
                lst.put(node.right)
        n = len(crs)
        if not crs:
            return root
        for i in range(1, int(math.log2(n) + 1)):
            row = []
            left = int(math.pow(2, i) - 1)
            right = int(math.pow(2, i + 1) - 1)
            row.extend(crs[left: right])
            for j in range(len(row) - 1):
                row[j].next = row[j + 1]
        return root


if __name__ == '__main__':
    if 1:
        n1 = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)
        n5 = Node(5)
        n6 = Node(6)
        n7 = Node(7)
        n1.left = n2
        n1.right = n3
        n2.left = n4
        n2.right = n5
        n3.left = n6
        n3.right = n7
        s = Solution()
        r = s.connect(n1)
    pass




