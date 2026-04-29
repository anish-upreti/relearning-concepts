class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        test_set = set(nums)

        ans = []
        for i in range(1, len(nums)+1):
            if i not in test_set:
                ans.append(i)
        return ans