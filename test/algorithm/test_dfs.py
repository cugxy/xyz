import unittest

from xyz.algorithm.dfs import DFS, Node


class TestCaseDFS(unittest.TestCase):

    def test_DFS0(self):
        d = DFS()
        r = d.dfs(None, 0)
        self.assertFalse(r)

    def test_DFS1(self):
        node_6 = Node(6, [])
        node_5 = Node(5, [node_6, ])
        node_4 = Node(4, [])
        node_3 = Node(3, [node_4, node_5])
        node_2 = Node(2, [])
        node_1 = Node(1, [node_2, ])
        node_0 = Node(0, [node_2, node_1, node_3])
        d = DFS()
        r = d.dfs(node_0, 0)
        self.assertTrue(r)

    def test_DFS2(self):
        node_6 = Node(6, [])
        node_5 = Node(5, [node_6, ])
        node_4 = Node(4, [])
        node_3 = Node(3, [node_4, node_5])
        node_2 = Node(2, [])
        node_1 = Node(1, [node_2, ])
        node_0 = Node(0, [node_2, node_1, node_3])
        d = DFS()
        r = d.dfs(node_0, 4)
        self.assertTrue(r)

    def test_DFS3(self):
        node_6 = Node(6, [])
        node_5 = Node(5, [node_6, ])
        node_4 = Node(4, [])
        node_3 = Node(3, [node_4, node_5])
        node_2 = Node(2, [])
        node_1 = Node(1, [node_2, ])
        node_0 = Node(0, [node_2, node_1, node_3])
        d = DFS()
        r = d.dfs(node_0, 7)
        self.assertFalse(r)


if __name__ == '__main__':
    unittest.main()
