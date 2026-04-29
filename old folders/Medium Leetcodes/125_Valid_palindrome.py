class Solution:
    def isPalindrome(self, s: str) -> bool:
        ans = "".join (ch for ch in s if ch.isalnum())
        
        if ans.lower() == ans[::-1].lower():
            return True
        else:
            return False
        

# Alternate solution
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l = 0
        r = len(s) - 1
        while l < r:
            if not s[l].isalnum():
                l += 1
                continue
            if not s[r].isalnum():
                r -= 1
                continue
            if s[l].lower() != s[r].lower():
                return False
            
            l += 1
            r -= 1
        return True

