G = [[0, 83, 53, 80, 57, 90, 64], 
    [94, 46, 98, 87, 54, 56, 46], 
    [84, 26, 35, 79, 33, 94, 76], 
    [22, 57, 20, 83, 90, 52, 99], 
    [56, 25, 49, 52, 38, 65, 36], 
    [29, 83, 54, 38, 47, 69, 82], 
    [31, 98, 83, 22, 56, 82, 0]]
S = 0
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
    for d in DIRS:
        max_profit_recurse(grid, n-1, n-1, s, d)
    return max(cache[n-1][n-1][s])

def no_sharp(grid, r, c, last):
    if -1 != cache[r][c][0][last]:
        return
    if r <= 1 and c <= 1:
        cache[r][c][0][last] = grid[r][c]
    elif r == 0:
        no_sharp(grid, r, c-1, RIGHT)
        cache[r][c][0][last] = cache[r][c-1][0][RIGHT] + grid[r][c]
    elif c == 0:
        no_sharp(grid, r-1, c, DOWN)
        cache[r][c][0][last] = cache[r-1][c][0][DOWN] + grid[r][c]
    elif r == 1:
        
    elif c == 1:
        pass
    else:
        for d in DIRS:
            no_sharp(grid, r, c-1, d) 
            no_sharp(grid, r-1, c-1, d) 
            no_sharp(grid, r-1, c, d) 

        if last == RIGHT:
            profits[cache[r][c-1][s][d] for d in DIRS]
        elif last == DOWN:
            profits = [cache[r-1][c][s][d] for d in DIRS]
        else:
            profits = [cache[r-1][c-1][s][d] for d in DIRS]

        cache[r][c][s][last] = max(profits) + grid[r][c]

def max_profit_recurse(grid, r, c, s, last):
    if -1 != cache[r][c][s][last]:
        return
    elif s == 0:
        no_sharp(grid, r, c, last)
        return
    if r == 0 and c == 0:
        cache[r][c][s][last] = 0
    elif r == 0:
        max_profit_recurse(grid, r, c-1, s, RIGHT)
        cache[r][c][s][last] = cache[r][c-1][s][RIGHT] + grid[r][c]
    elif c == 0:
        max_profit_recurse(grid, r-1, c, s, DOWN)
        cache[r][c][s][last] = cache[r-1][c][s][DOWN] + grid[r][c]
    else:
        for k in [s, s-1]:
            for d in DIRS:
                max_profit_recurse(grid, r, c-1, k, d) 
                max_profit_recurse(grid, r-1, c-1, k, d) 
                max_profit_recurse(grid, r-1, c, k, d) 

        if last == RIGHT:
            profits[cache[r][c-1][s][d] for d in DIRS]
        elif last == DOWN:
            profits = [cache[r-1][c][s][d] for d in DIRS]
        else:
            profits = [cache[r-1][c-1][s][d] for d in DIRS]

        cache[r][c][s][last] = max(profits) + grid[r][c]

print(max_profit(G, S))

import numpy as np
print(np.array(G))
print(np.array([[max(cell[S]) for cell in row] for row in cache]))
