# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       28
   Description :
   Author :          cugxy
   date：            2019/10/12
-------------------------------------------------
   Change Activity:
                     2019/10/12
-------------------------------------------------

继承 collection.abc 以实现自定义的容器类型
- 如果要定制的子类比较简单, 那就可以直接从 Python 的容器类型 (如 list 或 dict) 中继承
- 想要正确实现自定义的容器类型, 可能需要编写大量的特殊方法
- 编写自定义容器类型时, 可以从 collections.abc 模块的抽象基类中继承, 能够确保我们的子类具备适当的接口及行为

"""

from collections.abc import Sequence


class BinaryNode(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class IndexableNode(BinaryNode):
    def __init__(self, val, left=None, right=None):
        super().__init__(val, left, right)
        self._dfs()

    def __getitem__(self, item):
        found, _ = self._search(0, item)
        if not found:
            raise IndexError('Index out of range')
        return found.val

    def _dfs(self):
        node_stack = []
        self.dfs = []
        node_stack.append(self)
        while len(node_stack) > 0:
            node = node_stack.pop()
            self.dfs.append(node)
            if node.right:
                node_stack.append(node.right)
            if node.left:
                node_stack.append(node.left)

    def _search(self, count, item):
        return self.dfs[item], count


class SequenceNode(IndexableNode):
    def __len__(self):
        return len(self.dfs)


class BetterNode(SequenceNode, Sequence):
    pass


if __name__ == '__main__':
    if 1:
        tree = IndexableNode(10, left=IndexableNode(5, left=IndexableNode(2), right=IndexableNode(6, right=IndexableNode(7))), right=IndexableNode(15, left=IndexableNode(11)))
        print(tree[0])
        print(tree[1])

    pass
