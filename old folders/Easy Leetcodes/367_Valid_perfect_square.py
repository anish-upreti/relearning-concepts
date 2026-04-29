class Solution:
    def isPerfectSquare(self, num: int) -> bool:
        l = 1
        r = num

        while l <= r:
            m = (l + r)//2

            if m**2 == num:
                return True
            elif m**2 > num:
                r = m - 1
            else:
                l = m + 1
        
        return False