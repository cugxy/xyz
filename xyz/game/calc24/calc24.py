# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       calc24
   Description :
   Author :          cugxy
   date：            2019/7/19
-------------------------------------------------
   Change Activity:
                     2019/7/19
-------------------------------------------------
"""
import itertools
import math


class Node(object):
    def __init__(self, result=None):
        self._left = None
        self._rigth = None
        self._operator = None
        self._result = result

    def set_expression(self, left_node, right_node, operator):
        self._left = left_node
        self._right = right_node
        self._operator = operator
        expression = "{} {} {}".format(left_node._result, operator, right_node._result)
        self._result = eval(expression)
    
    def __repr__(self):
        if self._operator:
            return '<Node operator="{}">'.format(self._operator)
        else:
            return '<Node value="{}">'.format(self._result)


def build_all_trees(arr):
    rs = []
    if len(arr) == 1:
        tree = Node(arr[0])
        rs.append(tree)
        return rs
    for i in range(1, len(arr)):
        left_arr = arr[:i]
        right_arr = arr[i:]
        left_trees = build_all_trees(left_arr)
        right_trees = build_all_trees(right_arr)
        for l in left_trees:
            for r in right_trees:
                c_tree = build_tree(l, r)
                rs.extend(c_tree)
    return rs


def create_tree(l, r, op):
    t = Node()
    t.set_expression(l, r, op)
    return t


def build_tree(l, r):
    rs = []
    t1 = create_tree(l, r, '+')
    t2 = create_tree(l, r, '-')    
    t3 = create_tree(l, r, '*')
    rs.append(t1)
    rs.append(t2)
    rs.append(t3)
    if r._result != 0:
        t4 = create_tree(l, r, '/')
        rs.append(t4)
    return rs


def get_expression(tree):
    rs = []
    if tree._result is None and tree._operator is None:
        return rs
    if tree._operator:
        rs.append(tree._operator)
        l_rs = get_expression(tree._left)
        r_rs = get_expression(tree._right)
        rs.extend(l_rs)
        rs.extend(r_rs)
    if tree._operator is None and tree._result:
        rs.append(tree._result)
    return rs


def calc24(arr):
    expr = None
    perms = itertools.permutations(arr)
    found = False
    for perm in perms:
        t_rs = build_all_trees(perm)
        for t in t_rs:
            print(t._result)
            if math.isclose(t._result, 24, rel_tol=1e-10):
                expr = get_expression(t)
                expr = [str(e) for e in expr]
                print("{} | {}".format(perm, " ".join(expr)))
                found = True
                break
        if found:
            break
    return expr


if __name__ == '__main__':
    if 1:
        arr = [7, 3, 7, 3, ]
        calc24(arr)
