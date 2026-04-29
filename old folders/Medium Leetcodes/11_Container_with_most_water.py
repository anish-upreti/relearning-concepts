class Solution:
    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height) - 1
        max_water = 0
        while l<r:
            length = r - l
            heightt = min(height[l], height[r])
            water = length * heightt
            max_water = max(max_water, water)

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        
        return max_water

# time - O(n)
# space - O(1)