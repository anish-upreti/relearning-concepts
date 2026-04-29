class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        L = 0
        length = 0
        n = len(s)
        set1 =set()

        for R in range(n):
            while s[R] in set1:
                set1.remove(s[L])
                L+=1

            window = (R-L) + 1
            length = max(length, window)
            set1.add(s[R])

        return length
    
# Time - O(n) -- using varible length sliding window algorithm
