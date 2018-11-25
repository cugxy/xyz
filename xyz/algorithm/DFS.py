#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:
@file:  
@time: 
"""


class Node(object):
    def __init__(self, val, next_nodes):
        self.val = val
        self.next_nodes = next_nodes


class DFS(object):
    visited = []

    def dfs(self, node, v):
        '''
        深度优先搜索算法
        :param node:  根结点
        :param v:     目标值
        :return:      True | False
        '''
        self.visited.append(node)
        if v == node.val:
            return True
        for _node in node.next_nodes:
            if _node not in self.visited:
                if self.dfs(_node, v):
                    return True
            self.visited.remove(_node)
        return False


if __name__ == '__main__':
    node_6 = Node(6, [])
    node_5 = Node(5, [node_6, ])
    node_4 = Node(4, [])
    node_3 = Node(3, [node_4, node_5])
    node_2 = Node(2, [])
    node_1 = Node(1, [node_2, ])
    node_0 = Node(0, [node_2, node_1, node_3])
    d = DFS()
    r = d.dfs(node_0, 6)
    pass