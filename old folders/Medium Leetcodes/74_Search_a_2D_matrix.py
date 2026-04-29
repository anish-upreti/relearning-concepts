class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        L = 0
        m, n = len(matrix), len(matrix[0])
        R = (m*n) - 1

        while L <= R:
            M = (L+R)//2
            i = M//n
            j = M % n

            if matrix[i][j] == target:
                return True
            
            elif matrix[i][j] > target:
                R = M - 1
            else:
                L = M + 1

        return False

    ## time - O(log (m*n)) 