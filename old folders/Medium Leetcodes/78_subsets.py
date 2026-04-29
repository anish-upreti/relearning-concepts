class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        sol = []

        def backtrack(i):
            if i == len(nums):
                res.append(sol[:])
                return

            # pick num
            sol.append(nums[i])
            backtrack(i+1)

            # don't pick num
            sol.pop()
            backtrack(i+1)

        backtrack(0)
        return res
    
# Time - O(2^n) -- using recursive backtracking