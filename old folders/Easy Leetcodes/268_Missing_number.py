class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        nums.sort()

        for i,v in enumerate(nums):
            if i != v:
                return v-1

            if v == len(nums)-1:
                return v+1
            

# Alternate solution

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        sum_n = sum(range(len(nums)+1)) # or (n*(n+1))//2
        sum_list = sum(nums)
        return sum_n - sum_list