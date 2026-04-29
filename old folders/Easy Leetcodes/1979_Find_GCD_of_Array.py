class Solution:
    def findGCD(self, nums: List[int]) -> int:
        smallest = nums[0]
        largest = nums[0]

        for num in nums:
            if num < smallest:
                smallest = num
            
        for num in nums:
            if num > largest:
                largest = num

        def gcd(smallest, largest):
            if smallest==0:
              return largest
            return gcd(largest%smallest, smallest)
        return gcd(smallest, largest)
    

## Alternate solution
class Solution:
    def findGCD(self, nums: List[int]) -> int:

        smallest = min(nums)
        largest = max(nums)

        def gcd(smallest, largest):
            if smallest==0:
              return largest
            else:
                return gcd(largest%smallest, smallest)
        return gcd(smallest, largest)
            

