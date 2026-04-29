# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        
        def sameTree(p, q):
            if not p and not q:
                return True

            if (p and not q) or (q and not p):
                return False

            if p.val != q.val:
                return False

            return sameTree(p.left, q.left) and sameTree(p.right, q.right)

        def check_subtree(root):
            if not root:
                return False

            if sameTree(root, subRoot):
                return True

            return check_subtree(root.left) or check_subtree(root.right)

        return check_subtree(root)

    ## Time - O(m * n) -- where m is the number of nodes in root Tree
                        ## and n is the number of nodes in subRoot Tree

    ## space - O(m + n)