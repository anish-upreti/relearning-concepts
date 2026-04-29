class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        ans = []
        i, j = 0, 0
        up, right, down, left = 0, 1, 2, 3
        direction = right

        top_wall = 0
        right_wall = n
        down_wall = m
        left_wall = -1

        while len(ans) != m*n:
            if direction == right:
                while j < right_wall:
                    ans.append(matrix[i][j])
                    j += 1
                i, j = i+1, j-1
                right_wall -= 1
                direction = down
            elif direction == down:
                while i < down_wall:
                    ans.append(matrix[i][j])
                    i += 1
                i, j = i-1, j-1
                down_wall -= 1
                direction = left
            elif direction == left:
                while j > left_wall:
                    ans.append(matrix[i][j])
                    j -= 1
                i, j = i-1, j+1
                left_wall += 1
                direction = up
            else:
                while i > top_wall:
                    ans.append(matrix[i][j])
                    i -= 1
                i, j = i+1, j+1
                top_wall += 1
                direction = right
        
        return ans 
            



# alternate code

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        n, m = len(matrix), len(matrix[0])
        top, left, right, down = 0, 0, m - 1, n - 1

        while len(res) != n * m:
            for i in range(left, right + 1):
                res.append(matrix[top][i])

            for i in range(top + 1, down + 1):
                res.append(matrix[i][right])

            if top != down:
                for i in range(right - 1, left - 1, -1):
                    res.append(matrix[down][i])

            if left != right:
                for i in range(down - 1, top, -1):
                    res.append(matrix[i][left])

            top += 1
            left += 1
            right -= 1
            down -= 1

        return res