class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        
        if len(s) == 0: return True
        if len(s) > len(t): return False

        i = 0
        for letter in t:
            if s[i] == letter:
                i += 1
            if i == len(s):
                return True
        return False


