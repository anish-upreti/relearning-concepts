class Solution:
    def fib(self, n: int) -> int:
        
        # # General recursive method - Time O(n)
        # if n==0:
        #     return 0
        # elif n == 1:
        #     return 1
        # else:
        #     return self.fib(n-1) + self.fib(n-2)

        
        # Dynamic Programming - top down approach(memoizatin) - time- O(n)

        memo = {0:0, 1:1}

        def f(x):
            if x in memo:
                return memo[x]
            else:
                memo[x] = f(x-1) + f(x-2)
                return memo[x]

        return f(n)