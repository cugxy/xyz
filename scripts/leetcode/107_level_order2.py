#!usr/bin/env python  
# -*- coding:utf-8 _*-

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def levelOrderBottom(self, root):
        rs = self.levelOrder(root)
        return rs[::-1]
    
    def levelOrder(self, root):
        rs = []
        if root is None:
            return rs
        q = []
        q.append(root)
        while len(q) != 0:
            p = []
            for i in range(len(q)):
                node = q.pop(0)
                p.append(node.val)
                if node.left is not None:
                    q.append(node.left)
                if node.right is not None:
                    q.append(node.right)
            rs.append(p)
        return rs
    
if __name__ == '__main__':
    from IPython import embed
    n3 = TreeNode(3)
    n9 = TreeNode(9)
    n20 = TreeNode(20)
    n15 = TreeNode(15)
    n7 = TreeNode(7)
    n3.left = n9
    n3.right = n20
    n20.left = n15
    n20.right = n7
    s = Solution()
    r = s.levelOrderBottom(n3)
    print(r)
