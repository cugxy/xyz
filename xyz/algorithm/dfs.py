# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     dfs.py
   Description :
   Author :       cugxy
   date：          2019/5/19 0019
-------------------------------------------------
   Change Activity:
                   2019/5/19 0019:
-------------------------------------------------
"""


class Node(object):
    """Node"""
    def __init__(self, val, next_nodes):
        self.val = val
        self.next_nodes = next_nodes


class DFS(object):
    """
    DFS
    """
    visited = []

    def dfs(self, node, v):
        """
        深度优先搜索算法
        :param node:  根结点
        :param v:     目标值
        :return:      True | False
        """
        if node is None:
            return False
        self.visited.append(node)
        if v == node.val:
            return True
        for _node in node.next_nodes:
            if _node not in self.visited:
                if self.dfs(_node, v):
                    return True
            self.visited.remove(_node)
        return False
