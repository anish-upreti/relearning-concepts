class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        left = 1
        right = 1
        n = len(nums)
        l_arr = [1] * n
        r_arr = [1] * n

        for i in range(n):
            j = -i-1
            l_arr[i] = left
            r_arr[j] = right
            left *= nums[i]
            right *= nums[j]

        return [l*r for l,r in zip(l_arr, r_arr)]


# alternate code
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [1] * len(nums)
        n = len(nums)
        left = 1
        for i in range(n):
            result[i] *= left
            left *= nums[i]
        
        right = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right
            right *= nums[i]
    
        return result