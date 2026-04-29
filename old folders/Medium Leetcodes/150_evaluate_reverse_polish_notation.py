import math
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stk = []

        for item in tokens:
            if item in "+-/*":
                a = stk.pop(-2)
                b = stk.pop(-1)

                if item == "+":
                    stk.append(a + b)
                elif item == "-":
                    stk.append(a-b)
                elif item == "*":
                    stk.append(a*b)
                else:
                    div = a/b
                    if div < 0:
                        stk.append(math.ceil(div))
                    else:
                        stk.append(math.floor(div))
                    # or you can directly use stk.append(math.trunc(a/b)) or stk.append(int(a/b))

            else:
                stk.append(int(item))
            
        return stk[0]
