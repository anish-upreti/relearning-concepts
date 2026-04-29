class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        # validate rows
        for i in range(9):
            test_set = set()
            for j in range(9):
                num = board[i][j]
                if num in test_set:
                    return False
                elif num != ".":
                    test_set.add(num)

        # validate columns
        for i in range(9):
            test_set = set()
            for j in range(9):
                num = board[j][i]
                if num in test_set:
                    return False
                elif num != ".":
                    test_set.add(num)


        # validate 3x3 boxes
        index_list = [(0,0), (0, 3), (0,6),
                      (3,0), (3,3), (3,6),
                      (6,0), (6,3), (6,6)]

        for i, j in index_list:
            test_set = set()
            for row in range(i, i+3):
                for col in range(j, j+3):
                    num = board[row][col]
                    if num in test_set:
                        return False
                    elif num != ".":
                        test_set.add(num)
        
        return True
                