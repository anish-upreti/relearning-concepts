class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        s = set()

        for i in nums:
            if i in s:
                return True
            else:
                s.add(i)

        return False


# Alternate solution - using sort

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        nums.sort()

        for i in range(1, len(nums)):
            if nums[i] == nums[i-1]:
                return True
        
        return False
    
# Alternate solution
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        num_set = set(nums)
        
        if len(num_set) == len(nums):
            return False
        else:
            return True
    



