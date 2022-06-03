def read_grid(n):
    """This helper function reads n lines as a nxn grid.
    They are returned as a list of lists. 
    (You may replace this representation with something else if you want.)
    """
    grid = []
    for i in range(n):
        grid.append([])
        row = input().split(' ')
        for j in range(n):
            grid[i].append(int(row[j]))
    return grid

n = int(input())
G = read_grid(n)

#################################
# implement your algorithm here #
#################################
# print out the maximum profit using no sharp turns

cache = [[0 for i in range(n)] for i in range(n)]

def max_profit(grid):
    max_profit_recurse(grid, 0, 0, None)
    return cache[n-1][n-1]

def max_profit_recurse(grid, r, c, last_move):
    if r == n or c == n:
        return

    if r == 0 and c == 0:
        cache[r][c] == grid[r][c]
        max_profit_recurse(grid, r+1, c, "down")
        max_profit_recurse(grid, r, c+1, "right")
        max_profit_recurse(grid, r+1, c+1, "diag")
        return

    if last_move == "down":
        if r == n-1 and c != n-1:
            return
        path_profit = cache[r-1][c] + grid[r][c]
        if path_profit > cache[r][c]:
            cache[r][c] = path_profit
            max_profit_recurse(grid, r+1, c, "down")
            max_profit_recurse(grid, r+1, c+1, "diag")
    elif last_move == "right":
        if r != n-1 and c == n-1:
            return
        path_profit = cache[r][c-1] + grid[r][c]
        if path_profit > cache[r][c]:
            cache[r][c] = path_profit
            max_profit_recurse(grid, r, c+1, "right")
            max_profit_recurse(grid, r+1, c+1, "diag")
    elif last_move == "diag":
        path_profit = cache[r-1][c-1] + grid[r][c]
        if path_profit > cache[r][c]:
            cache[r][c] = path_profit
            max_profit_recurse(grid, r+1, c, "down")
            max_profit_recurse(grid, r, c+1, "right")
            max_profit_recurse(grid, r+1, c+1, "diag")

print(max_profit(G))