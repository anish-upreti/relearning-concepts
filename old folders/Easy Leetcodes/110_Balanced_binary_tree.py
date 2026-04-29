# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        balanced = [True]

        def height(root):
            if root is None:
                return 0

            l_height = height(root.left)
            r_height = height(root.right)

            if abs(l_height - r_height) > 1:
                balanced[0] = False
                return 0

            return 1 + max(l_height, r_height)

        height(root)
        return balanced[0]
    
## Time - O(n)
## space - O(h)