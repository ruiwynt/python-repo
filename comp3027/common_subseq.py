import numpy as np

def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.read().split()))

arr1 = None
arr2 = None
cache = None

def max_cs(i, j):
    if cache[i+1][j+1] != -1:
        return cache[i+1][j+1].copy()

    if i == -1 or j == -1:
        cache[i+1][j+1] = []
        return []

    discard_i = max_cs(i-1, j)
    discard_j = max_cs(i, j-1)
    if arr1[i] == arr2[j]:
        choose = max_cs(i-1, j-1)
        m = max(len(choose)+1, len(discard_i), len(discard_j))
        if m == len(choose)+1:
            cache[i+1][j+1] = cache[i][j] + [arr1[i]]
        elif m == len(discard_i):
            cache[i+1][j+1] = cache[i][j+1].copy()
        else:
            cache[i+1][j+1] = cache[i+1][j].copy()
    elif arr1[i] != arr2[j]:
        m = max(len(discard_i), len(discard_j))
        if m == len(discard_i):
            cache[i+1][j+1] = cache[i][j+1].copy()
        else:
            cache[i+1][j+1] = cache[i+1][j].copy()
    return cache[i+1][j+1]

if __name__ == "__main__":
    arr1 = get_arr("arr.txt")
    arr2 = get_arr("arr1.txt")
    cache = [[-1 for _ in range(len(arr2)+1)] for _ in range(len(arr1)+1)]
    m = len(arr1)-1
    n = len(arr2)-1
    max_cs(m, n)
    # print(cache)
    print(f"Maximum Common Subarray: {cache[m+1][n+1]}")
    print(f"Maximum Common Subarray Length: {len(cache[m+1][n+1])}")
