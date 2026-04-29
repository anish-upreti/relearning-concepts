
class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        b_dict = {}
        balloon = "balloon"

        for char in text:
            if char in balloon:
                b_dict[char] = b_dict.get(char, 0) +1

        if any(char not in b_dict for char in balloon):
            return 0
        else:
            return min(b_dict["b"], b_dict["a"], b_dict["l"]//2, b_dict["o"]//2, b_dict["n"])

            

# Solution using defaultdict
class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        b_dict = defaultdict(int)
        balloon = "balloon"

        for char in text:
            if char in balloon:
                b_dict[char] += 1

        return min(b_dict["b"], b_dict["a"], b_dict["l"]//2, b_dict["o"]//2, b_dict["n"])

            