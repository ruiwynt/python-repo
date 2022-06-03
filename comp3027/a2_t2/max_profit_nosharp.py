G = [[0, 83, 53, 80, 57, 90, 64], [94, 46, 98, 87, 54, 56, 46], [84, 26, 35, 79, 33, 94, 76], [22, 57, 20, 83, 90, 52, 99], [56, 25, 49, 52, 38, 65, 36], [29, 83, 54, 38, 47, 69, 82], [31, 98, 83, 22, 56, 82, 0]]
n = 7

#################################
# implement your algorithm here #
#################################
# print out the maximum profit using no sharp turns

cache = [[(0, None) for i in range(n)] for i in range(n)]

profit = lambda x: x[0]
last = lambda x: x[1]

def max_profit(grid):
    max_profit_recurse(grid, 0, 0, None)
    return print(profit(cache[n-1][n-1]))

def max_profit_recurse(grid, r, c, last_move):
    if r == n or c == n:
        return

    if r == 0 and c == 0:
        cache[r][c] == (grid[r][c], None)
        max_profit_recurse(grid, r+1, c, "down")
        max_profit_recurse(grid, r, c+1, "right")
        max_profit_recurse(grid, r+1, c+1, "diag")
        return

    if last_move == "down":
        if r == n-1 and c != n-1:
            return
        path_profit = profit(cache[r-1][c]) + grid[r][c]
        if path_profit > profit(cache[r][c]):
            cache[r][c] = (path_profit, "down")
            max_profit_recurse(grid, r+1, c, "down")
            max_profit_recurse(grid, r+1, c+1, "diag")
    elif last_move == "right":
        if r != n-1 and c == n-1:
            return
        path_profit = profit(cache[r][c-1]) + grid[r][c]
        if path_profit > profit(cache[r][c]):
            cache[r][c] = (path_profit, "right")
            max_profit_recurse(grid, r, c+1, "right")
            max_profit_recurse(grid, r+1, c+1, "diag")
    elif last_move == "diag":
        path_profit = profit(cache[r-1][c-1]) + grid[r][c]
        if path_profit > profit(cache[r][c]):
            cache[r][c] = (path_profit, "diag")
            max_profit_recurse(grid, r+1, c, "down")
            max_profit_recurse(grid, r, c+1, "right")
            max_profit_recurse(grid, r+1, c+1, "diag")

print(max_profit(G))
import numpy as np
print(np.array(G))
print(np.array([list(map(profit, cache[i])) for i in range(n)]))
print(np.array([list(map(last, cache[i])) for i in range(n)]))
