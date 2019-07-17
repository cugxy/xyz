"""
给定一个二叉树和一个目标和，找到所有从根节点到叶子节点路径总和等于给定目标和的路径。

说明: 叶子节点是指没有子节点的节点。

示例:
给定如下二叉树，以及目标和 sum = 22，

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
返回:

[
   [5,4,11,2],
   [5,8,4,5]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/path-sum-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def __init__(self):
        self.tmp = 0
        self.rs = []

    def pathSum(self, root, sum):
        pass
    
    def func(self, root, sum):
        if root is None:
            return self.rs
        if root.left is None and root.right == None:
            if sum - root.val == 0:
                tmp_rs = []
                tmp_rs.append(root.val)
                self.rs.append(tmp_rs)
                return self.rs
        if root.left is not None:
            rs_left = self.func(root.left, sum-root.val)
            for 


        

if __name__ == '__main__':
    if 1:
        s = Solution()
        root = TreeNode(5)
        n4 = TreeNode(4)
        n8 = TreeNode(8)
        n11 = TreeNode(11)
        n13 = TreeNode(13)
        n41 = TreeNode(4)
        n7 = TreeNode(7)
        n2 = TreeNode(2)
        n5 = TreeNode(5)
        n1 = TreeNode(1)
        root.left = n4
        root.right = n8
        n4.left = n11
        n8.left = n13
        n8.right = n41
        n11.left = n7
        n11.right = n2
        n4.left = n5
        n4.right = n1
        sum = 22
        r = s.pathSum(root, sum)
        print(r)