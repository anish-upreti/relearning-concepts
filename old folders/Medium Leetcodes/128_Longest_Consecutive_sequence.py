class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        test_set = set(nums)
        longest = 0

        for num in test_set:
            if num-1 not in test_set:
                len = 1
                next = num + 1
                while next in test_set:
                    next += 1
                    len += 1
                longest = max(len, longest)

        return longest

    # time - O(n)