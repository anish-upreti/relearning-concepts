## Brute force type solution

class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        count = 0

        for i in range(len(stones)):
            if stones[i] in jewels:
                count += 1


        return count
    # time - O(length of jewels * length of stones)

# Efficient Solution
class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        count = 0
        s = set(jewels)

        for stone in stones:
            if stones in s:  # looking for an element in a set(hash table) is a constant time operation i.e O(1)
                count += 1


        return count
    #time - O(length of jewels * length of stones)
