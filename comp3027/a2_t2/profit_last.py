G = [[0, 83, 53, 80, 57, 90, 64], 
    [94, 46, 98, 87, 54, 56, 46], 
    [84, 26, 35, 79, 33, 94, 76], 
    [22, 57, 20, 83, 90, 52, 99], 
    [56, 25, 49, 52, 38, 65, 36], 
    [29, 83, 54, 38, 47, 69, 82], 
    [31, 98, 83, 22, 56, 82, 0]]
S = 4
n = 7

#################################
# implement your algorithm here #
#################################
# print out the maximum profit using some sharp turns

# cache[DIRECTION][i][j] = (OPT[i][j], last_move)
DOWN = 0
RIGHT = 1
DIAG = 2
DIRS = (DOWN, RIGHT, DIAG)

cache = [[[[-1, -1, -1] for i in range(S+1)] for j in range(n)] for k in range(n)]

def max_profit(grid, s):
    max_profit_recurse(grid, n-1, n-1, s)
    return max(cache[n-1][n-1][s])

def max_profit_recurse(grid, r, c, s):
    if cache[r][c][s] != [-1, -1, -1]:
        return
    if r == 0 and c == 0:
        for d in DIRS:
            cache[r][c][s][d] = 0
    elif r == 0:
        max_profit_recurse(grid, r, c-1, s)
        cache[r][c][s][RIGHT] = cache[r][c-1][s][RIGHT] + grid[r][c]
    elif c == 0:
        max_profit_recurse(grid, r-1, c, s)
        cache[r][c][s][DOWN] = cache[r-1][c][s][DOWN] + grid[r][c]
    else:
        for k in (s, s-1):
            max_profit_recurse(grid, r, c-1, k) 
            max_profit_recurse(grid, r-1, c-1, k) 
            max_profit_recurse(grid, r-1, c, k) 
        right_profits = [cache[r][c-1][s][RIGHT], cache[r][c-1][s][DIAG]]
        if s > 0:
            right_profits.append(cache[r][c-1][s-1][DOWN])
        cache[r][c][s][RIGHT] = max(right_profits) + grid[r][c]

        down_profits = [cache[r-1][c][s][DOWN], cache[r-1][c][s][DIAG]]
        if s > 0:
            down_profits.append(cache[r-1][c][s-1][RIGHT])
        cache[r][c][s][DOWN] = max(down_profits) + grid[r][c]

        cache[r][c][s][DIAG] = max([cache[r-1][c-1][s][d] for d in DIRS]) + grid[r][c]


import numpy as np
print(max_profit(G, S))
print(np.array(G))
print(np.array([[max(cell[S]) for cell in row] for row in cache]))
