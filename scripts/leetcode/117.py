# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       117.py
   Description :
   Author :          cugxy
   date：            2019/10/30
-------------------------------------------------
   Change Activity:
                     2019/10/30
-------------------------------------------------

给定一个二叉树

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
- 队列中 pop 一个节点, 并写入结果字典保存, 并记录层级, 同时让该节点的 孩子入队列,
- 重复上述操作

111 题目解答中 有更好的 层次遍历解决方案

"""


# Definition for a Node.
import queue


class Node:
    def __init__(self, val, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class Solution:
    def connect(self, root: Node) -> Node:
        if not root:
            return root
        lst = queue.Queue()
        crs = []
        setattr(root, 'level', 0)
        lst.put(root)
        while not lst.empty():
            node = lst.get()
            level = node.level
            crs.append(node)
            if node.left:
                setattr(node.left, 'level', level + 1)
                lst.put(node.left)
            if node.right:
                setattr(node.right, 'level', level + 1)
                lst.put(node.right)
        if not crs:
            return root
        for idx in range(1, len(crs) - 1):
            first = crs[idx]
            next = crs[idx + 1]
            if first.level == next.level:
                first.next = next
        return root


if __name__ == '__main__':
    if 1:
        n1 = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)
        n5 = Node(5)
        n7 = Node(7)
        n1.left = n2
        n1.right = n3
        n2.left = n4
        n2.right = n5
        n3.right = n7
        s = Solution()
        r = s.connect(n1)
    pass


