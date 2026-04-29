class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        test_dict = {}
        majority = 0
        ans = 0
        for num in nums:
            if num not in test_dict:
                test_dict[num] = 1
            else:
                test_dict[num] += 1

            if test_dict[num] > majority:
                ans = num
                majority = test_dict[num]

        return ans
    

# Alternate solution
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        test_dict = {}
        majority = 0
        ans = 0
        for num in nums:
            if num not in test_dict:
                test_dict[num] = 1
            else:
                test_dict[num] += 1

        for key, value in test_dict.items():
            if value > majority:
                majority = value
                ans = key

        return ans


# Efficient solution
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        count = 0
        ans = 0

        for num in nums:
            if count == 0:
                ans = num

            if ans == num:
                count += 1
            else:
                count -= 1

        return ans

        


        
