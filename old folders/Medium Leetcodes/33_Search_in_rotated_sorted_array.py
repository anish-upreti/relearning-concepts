class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l = 0
        n = len(nums)
        r = n - 1

        while l < r:
            m = (l + r)//2

            if nums[m] > nums[r]:
                l = m + 1
            else:
                r = m

        min_index = l
        if min_index == 0:
            l, r = 0, n - 1
        elif nums[0] <= target <= nums[min_index-1]:
            l, r = 0, min_index - 1
        else:
            l, r = min_index, n-1

        while l <= r:
            m = (l + r)//2
            
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1

        return -1
    

## Alternate solution
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        l = 0
        n = len(nums)
        r = n - 1

        while l<=r:
            m = (l + r)//2

            if nums[m] == target:
                return m
            elif nums[m] >= nums[l]:
                if nums[l] <= target <= nums[m]:
                    r = m - 1
                else:
                    l = m + 1
            else:
                if nums[m] <= target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1

        return -1

            