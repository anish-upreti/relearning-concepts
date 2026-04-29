class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        count_dict = {}
        for c in magazine:
            if c not in count_dict:
                count_dict[c] = 1
            else:
                count_dict[c] += 1

        for c in ransomNote:
            if c not in count_dict:
                return False
            elif count_dict[c] == 1:
                del count_dict[c]
            else:
                count_dict[c] -= 1

        return True
    # time - O(length of magazine + length of ransomNote)



# Solution using Counter
from collections import Counter
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        count_dict = Counter(magazine)

        for c in ransomNote:
            if c not in count_dict:
                return False
            elif count_dict[c] == 1:
                del count_dict[c]
            else:
                count_dict[c] -= 1

        return True
    
    
# Alternate solution
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        count_dict = defaultdict(int) # assigns value zero by dafault for new key in dictionary

        for c in magazine:
            count_dict[c] += 1

        for c in ransomNote:
            if c not in count_dict:
                return False
            elif count_dict[c] == 1:
                del count_dict[c]
            else:
                count_dict[c] -= 1

        return True
    

