# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        max_diameter = [0]

        def find_height(root):
            if root is None:
                return 0
            l_height = find_height(root.left)
            r_height = find_height(root.right)
            curr_diameter = l_height + r_height

            max_diameter[0] = max(max_diameter[0], curr_diameter)

            return 1 + max(l_height, r_height)

        find_height(root)

        return max_diameter[0]
    
## Time - O(n)
## space - O(h) or O(n)