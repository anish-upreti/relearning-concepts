class Solution:
    def isValid(self, s: str) -> bool:
        stk = []
        hash_map = {")":"(", "}":"{", "]":"["}
        
        for ch in s:
            if ch not in hash_map:  # if ch in hash_map.values():
                stk.append(ch)
            else:
                if not stk or stk.pop() != hash_map[ch]:
                    return False
        
        return not stk
    
## Alternate solution
class Solution:
    def isValid(self, s: str) -> bool:

        stk = []

        for i in range(len(s)):
            if stk:
                last = stk[-1]
                if self.compare(last, s[i]):
                    stk.pop()
                    continue
            stk.append(s[i])
        
        return not stk

    def compare(self, last, cur):
        if last == "(" and cur == ")" or last == "{" and cur == "}" or last == "[" and cur == "]":
            return True
        return False