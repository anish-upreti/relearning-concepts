class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stk = []
        ans = [0] * len(temperatures)

        for i in range(len(temperatures)):
            while stk and temperatures[stk[-1]] < temperatures[i]:
                idx = stk.pop()
                ans[idx] = i - idx
            stk.append(i)

        return ans
    
    ## time - O(n)
    ## space - O(n)
    

## Alternate solution -- appending tuple in stack
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stk = []
        ans = [0] * len(temperatures)

        for i,t in enumerate(temperatures):
            while stk and stk[-1][0] < t:
                stk_t, stk_i = stk.pop()
                ans[stk_i] = i - stk_i
            stk.append((t,i))

        return ans