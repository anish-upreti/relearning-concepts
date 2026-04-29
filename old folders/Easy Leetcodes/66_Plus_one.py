class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        # loop through the list from last to first element
        for i in range(len(digits)-1, -1, -1):
            # if current digit is 9, make it 0
            if digits[i] == 9:
                digits[i] = 0
            else:
                # if the digit is less than 9, increment it by 1 and return the list
                digits[i] = digits[i] + 1
                return digits
        # if all the elements are 9, then insert 1 at the beginning of the list
        return [1] + digits
    

## Time - O(n)
## space - O(1)