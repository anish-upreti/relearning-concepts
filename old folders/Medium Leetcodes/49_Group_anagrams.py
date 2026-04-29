from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Brute force approach
        anagram_dict = defaultdict(list)

        for string in strs:
            key ="".join(sorted(string))
            anagram_dict[key].append(string)

        return list(anagram_dict.values())

        

# Efficient solution
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_dict = defaultdict(list)

        for string in strs:
            count = [0] * 26
            for char in string:
                count[ord(char) - ord("a")] += 1 
            key = tuple(count)
            anagram_dict[key].append(string)

        return list(anagram_dict.values())


        