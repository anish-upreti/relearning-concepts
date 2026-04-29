## Using list as a stack

class Solution:
    def calPoints(self, operations: List[str]) -> int:
        list1 = []
        for item in operations:
            if item == "+":
                list1.append(list1[-1] + list1[-2])
            elif item == "C":
                list1.pop()
            elif item == "D":
                list1.append(list1[-1] * 2)
            else:
                list1.append(int(item))

        return sum(list1)
    

## Alternate solution
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        list1 = []
        for i in range(len(operations)):
            if operations[i] == "+":
                list1.append(list1[-2] + list1[-1])
            elif operations[i] == "D":
                list1.append(2*list1[-1])
            elif operations[i] == "C":
                list1.pop()
            else:
                list1.append(int(operations[i]))

            
        return sum(list1)