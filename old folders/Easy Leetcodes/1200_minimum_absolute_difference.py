class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        n = len(arr)
        
        min_diff = float("inf")
        for i in range(1, n):
            min_diff = min(min_diff, arr[i]-arr[i-1])
            
        ans = []
        for i in range(n-1):
            if abs(arr[i] - arr[i+1]) == min_diff:
                ans.append([arr[i], arr[i+1]])

        return ans