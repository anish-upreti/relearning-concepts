class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        test_set = set()

        for i, num in enumerate(nums):
            if num in test_set:
                return True
            test_set.add(num)

            if len(test_set) > k:
                test_set.remove(nums[i-k])

        return False