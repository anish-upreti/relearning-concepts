class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        triplets = []
        nums.sort()

        for i,v in enumerate(nums):

            if (i> 0) and (nums[i] == nums[i-1]):
                continue
            
            left = i + 1
            right = len(nums) - 1

            while left < right:
                curr_sum = v + nums[left] + nums[right]

                if curr_sum < 0:
                    left += 1
                elif curr_sum > 0:
                    right -= 1
                else:
                    triplets.append([v, nums[left], nums[right]])
                    left += 1

                    while (left < right) and (nums[left] == nums[left-1]):
                        left += 1
                    while (left < right) and (nums[right] == nums[right-1]):
                        right -= 1

        return triplets
    


# Alternate solution

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        ans = []
        nums.sort()

        for i in range(len(nums)):
            if nums[i] > 0:
                break
            elif i > 0 and nums[i] == nums[i-1]:
                continue
            l = i + 1
            r = len(nums) - 1

            while l < r:
                sum1 = nums[i] + nums[l] + nums[r]
                if sum1 == 0:
                    ans.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l<r and nums[l] == nums[l-1]:
                        l += 1
                    while l<r and nums[r] == nums[r+1]:
                        r -= 1
    
                elif sum1 < 0:
                    l += 1
                else:
                    r -= 1
        
        return ans