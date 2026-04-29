# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        # using BFS

        if root is None:
            return 0

        # Initializing queue with root node and its depth
        queue = [(root, 1)]

        while queue:
            node, depth = queue.pop(0)

            # returning the depth in case of leaf node
            if node.left is None and node.right is None:
                return depth

            # Enqueue the left and right nodes if they exist
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))

    ## Time - O(n)
    ## space - O(maximum width of the tree)


## Alternate solution
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:

        if root is None:
            return 0

        if root.left is None and root.right is None:
            return 1

        if root.left is None:
            return 1 + self.minDepth(root.right)

        if root.right is None:
            return 1 + self.minDepth(root.left)

        return 1 + min(self.minDepth(root.left), self.minDepth(root.right))
            