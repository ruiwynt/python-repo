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
import numpy as np

template = {"left": -1, "up": -1, "diag": -1}
s_cache = [template.copy() for i in range(S+1)]
row = [s_cache.copy() for i in range(n)]
cache = [row.copy() for i in range(n)]

dirs = template.keys()

vals = [[0 for i in range(n)] for j in range(n)]

def profit(x):
    max_p = max([x[key] for key in x.keys()])
    return (list(x.keys())[list(x.values()).index(max_p)], max_p)

def max_profit(grid, S):
    max_profit_recurse(grid,n-1, n-1, S)
    vals[n-1][n-1] = profit(cache[n-1][n-1][S])[1]
    return profit(cache[n-1][n-1][S])[1]

def max_profit_recurse(grid, r, c, turns):
    if list(cache[r][c][turns].items()) != [-1, -1, -1]:
        return

    if r == 0 and c == 0:
        for s in range(turns+1):
            for direction in dirs:
                cache[r][c][s][direction] = 0
    elif r == 0:
        for s in range(turns+1):
            max_profit_recurse(grid, r, c-1, s)
        cache[r][c][s]["left"] = cache[r][c-1][s]["left"] + grid[r][c]
        vals[r][c] = cache[r][c][turns]["left"]
    elif c == 0:
        for s in range(turns+1):
            max_profit_recurse(grid, r-1, c, s)
            cache[r][c][s]["up"] = cache[r-1][c][s]["up"] + grid[r][c]
        vals[r][c] = cache[r][c][turns]["up"]
    else:
        for s in range(turns+1):
            max_profit_recurse(grid, r-1, c, s)
            max_profit_recurse(grid, r, c-1, s)
            max_profit_recurse(grid, r-1, c-1, s)

        s = turns

        # Determine best path from above
        above = cache[r-1][c]
        best_profits = [above[s]["up"], above[s]["diag"]]
        if s > 0:
            best_profits.append(above[s-1]["left"])
        best_above = max(best_profits)
        cache[r][c][s]["up"] = best_above + grid[r][c]

        # Determine best path from left
        left = cache[r][c-1]
        best_profits = [left[s]["left"], left[s]["diag"]]
        if s > 0:
            best_profits.append(left[s-1]["up"])
        best_left = max(best_profits) 
        cache[r][c][s]["left"] = best_left + grid[r][c]

        # Determine best path from diag
        diag = cache[r-1][c-1]
        best_diag = max([diag[s][d] for d in ("diag", "left", "up")])
        cache[r][c][s]["diag"] = best_diag + grid[r][c]

        vals[r][c] = max(best_above, best_left, best_diag)


print(max_profit(G, S))
print(np.array(vals))
