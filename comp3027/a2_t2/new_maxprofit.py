G = [[0, 83, 53, 80, 57, 90, 64], [94, 46, 98, 87, 54, 56, 46], [84, 26, 35, 79, 33, 94, 76], [22, 57, 20, 83, 90, 52, 99], [56, 25, 49, 52, 38, 65, 36], [29, 83, 54, 38, 47, 69, 82], [31, 98, 83, 22, 56, 82, 0]]
n = 7
cache = [[((-1, None), (-1, None), (-1, None)) for i in range(n)] for i in range(n)]

profit = lambda x: x[0]
last = lambda x: x[1]
UP = 0
LEFT = 1
DIAG = 2

def best_profit(cell):
    profits = [profit(cell[i]) for i in range(3)]
    return max(profits)

def max_profit(grid):
    max_profit_recurse(grid, n-1, n-1)
    return max([profit(cache[n-1][n-1][i]) for i in range(3)])

def max_profit_recurse(grid, r, c):
    if max([profit(cache[r][c][i]) for i in range(3)]) != -1:
        return

    if r == 0 and c == 0:
        cache[0][0] = ((0, None), (0, None), (0, None))
    elif c == 0:
        max_profit_recurse(grid, r-1, c)
        cache[r][c] = ((profit(cache[r-1][c][UP]) + grid[r][c], "down"), (-1, None), (-1, None))
    elif r == 0:
        max_profit_recurse(grid, r, c-1)
        cache[r][c] = ((-1, None), (profit(cache[r][c-1][LEFT]) + grid[r][c], "right"), (-1, None))
    else:
        max_profit_recurse(grid, r-1, c)
        max_profit_recurse(grid, r, c-1)
        max_profit_recurse(grid, r-1, c-1)

        up_profit = max(profit(cache[r-1][c][UP]), profit(cache[r-1][c][DIAG]))
        left_profit = max(profit(cache[r][c-1][LEFT]), profit(cache[r][c-1][DIAG]))
        diag_profit = max(profit(cache[r-1][c-1][UP]), profit(cache[r-1][c-1][LEFT]), profit(cache[r-1][c-1][DIAG]))

        cache[r][c] = ((up_profit + grid[r][c], "down"), (left_profit + grid[r][c], "right"), (diag_profit + grid[r][c], "diag"))

print(max_profit(G))
import numpy as np
print(np.array(G))
print(np.array([list(map(best_profit, cache[i])) for i in range(n)]))
# print(np.array([list(map(last, cache[i])) for i in range(n)]))
