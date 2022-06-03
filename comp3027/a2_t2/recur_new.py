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

import numpy as np
cache = [[[-1 for i in range(S+1)] for j in range(n)] for k in range(n)]

def max_profit(grid, turns):
    max_profit_recurse(grid,n-1, n-1, turns)
    return cache[n-1][n-1][turns]

def no_sharp(grid, r, c):
    if cache[r][c][0] != -1 or r < 0 or c < 0:
        return

    if r <= 1 and c <= 1:
        cache[r][c][0] = grid[r][c]
        return
    elif r == 0:
        no_sharp(grid, r, c-1)
        cache[r][c][0] = cache[r][c-1][0] + grid[r][c]
        return
    elif c == 0:
        no_sharp(grid, r-1, c)
        cache[r][c][0] = cache[r-1][c][0] + grid[r][c]
        return
    elif r == 1 and c == 2:
        cache[r][c][0] = max(grid[0][1], grid[1][1]) + grid[r][c]
        return
    elif r == 2 and c == 1:
        cache[r][c][0] = max(grid[1][0], grid[1][1]) + grid[r][c]
        return
    elif r == 1:
        no_sharp(grid, r, c-2)
        no_sharp(grid, r-1, c-1)
        no_sharp(grid, r-1, c-2)
        cache[r][c][0] = max(cache[r][c-2][0] + grid[r][c-1], cache[r-1][c-2][0] + grid[r][c-1], cache[r-1][c-1][0]) + grid[r][c]
    elif c == 1:
        no_sharp(grid, r-2, c)
        no_sharp(grid, r-1, c-1)
        no_sharp(grid, r-2, c-1)
        cache[r][c][0] = max(cache[r-2][c][0] + grid[r-1][c], cache[r-2][c-1][0] + grid[r-1][c], cache[r-1][c-1][0]) + grid[r][c]
        return

    for i in (r-2, r-1, r):
        for j in (c-2, c-1, c):
            if not (i == r and j == c):
                no_sharp(grid, i, j)
    if r == 2 and c == 2:
        cache[r][c][0] = max(cache[1][1][0], cache[1][2][0], cache[2][1][0]) + grid[r][c]
    elif r == 2:
        cache[r][c][0] = max(
                cache[r-1][c-1][0], 
                cache[r][c-2][0] + grid[r][c-1],
                cache[r-1][c-2][0] + grid[r][c-1],
                cache[r-2][c-1][0] + grid[r-1][c]
                ) + grid[r][c]
    elif c == 2:
        cache[r][c][0] = max(
                cache[r-1][c-1][0],
                cache[r-1][c-2][0] + grid[r][c-1],
                cache[r-2][c-1][0] + grid[r-1][c],
                cache[r-2][c][0] + grid[r-1][c]
                ) + grid[r][c]
    else:
        cache[r][c][0] = max(
                cache[r-1][c-1][0],
                cache[r][c-2][0] + grid[r][c-1],
                cache[r-2][c-1][0] + grid[r-1][c],
                cache[r-1][c-2][0] + grid[r][c-1],
                cache[r-2][c][0] + grid[r-1][c]
                ) + grid[r][c]

def max_profit_recurse(grid, r, c, s):
    if s < 0 or cache[r][c][s] != -1:
        return
    if s == 0:
        no_sharp(grid, r, c)
        return
    # print(r, c, s)
    if r <= 1 and c <= 1:
        if s > 0 and r == 1 and c == 1:
            cache[r][c][s] = max(grid[r-1][c], grid[r][c-1]) + grid[r][c]
        else:
            cache[r][c][s] = grid[r][c]
    elif r == 0:
        max_profit_recurse(grid, r, c-1, s)
        cache[r][c][s] = cache[r][c-1][s] + grid[r][c]
    elif c == 0:
        max_profit_recurse(grid, r-1, c, s)
        cache[r][c][s] = cache[r-1][c][s] + grid[r][c]
    elif r == 1:
        for i in (r-1, r):
            for j in (c-2, c-1, c):
                if not (i == r and j == c):
                    max_profit_recurse(grid, i, j, s)
                    max_profit_recurse(grid, i, j, s-1)
        if s > 0:
            cache[r][c][s] = max(
                        cache[r-1][c][s-1],
                        cache[r-1][c-1][s],
                        max(cache[r-1][c-1][s-1], cache[r-1][c-2][s], cache[r][c-2][s]) + grid[r][c-1]
                    ) + grid[r][c] 
        else: 
            if c > 2:
                cache[r][c][s] = max(
                            cache[r-1][c-1][s],
                            max(cache[r-1][c-2][s], cache[r][c-2][s]) + grid[r][c-1]
                        ) + grid[r][c]
            else:
                cache[r][c][s] = max(grid[0][1], grid[1][1]) + grid[r][c]
    elif c == 1:
        for i in (r-2, r-1, r):
            for j in (c-1, c):
                if not (i == r and j == c):
                    max_profit_recurse(grid, i, j, s)
                    max_profit_recurse(grid, i, j, s-1)
        if s > 0:
            cache[r][c][s] = max(
                        cache[r][c-1][s-1],
                        cache[r-1][c-1][s],
                        max(cache[r-1][c-1][s-1], cache[r-2][c-1][s], cache[r-2][c][s]) + grid[r-1][c]
                    ) + grid[r][c] 
        else: 
            if r > 2:
                cache[r][c][s] = max(
                            cache[r-1][c-1][s],
                            max(cache[r-2][c-1][s], cache[r-2][c][s]) + grid[r-1][c]
                        ) + grid[r][c]
            else:
                cache[r][c][s] = max(grid[1][0], grid[1][1]) + grid[r][c]
    elif r == 2 and s == 0:
        if c == 2:
            cache[r][c][s] = max(grid[1][0] + grid[2][1], grid[1][1], grid[0][1] + grid[1][2]) + grid[r][c]
    else:
        for i in (r-2, r-1, r):
            for j in (c-2, c-1, c):
                if not (i == r and j == c):
                    max_profit_recurse(grid, i, j, s)
                    max_profit_recurse(grid, i, j, s-1)

        if s > 0:
            cache[r][c][s] = max(
                        max(cache[r-1][c-1][s-1], cache[r-1][c-2][s], cache[r][c-2][s]) + grid[r][c-1],
                        max(cache[r-1][c-1][s-1], cache[r-2][c-1][s], cache[r-2][c][s]) + grid[r-1][c],
                        cache[r-1][c-1][s]
                    ) + grid[r][c] 
        else:
            cache[r][c][s] = max(
                        max(cache[r-1][c-2][s], cache[r][c-2][s]) + grid[r][c-1],
                        max(cache[r-2][c-1][s], cache[r-2][c][s]) + grid[r-1][c],
                        cache[r-1][c-1][s]
                    ) + grid[r][c]

print(max_profit(G, S))
print(np.array(G))
print(np.array([[cell[S] for cell in row] for row in cache]))
print(np.array([[cell[S-1] for cell in row] for row in cache]))
