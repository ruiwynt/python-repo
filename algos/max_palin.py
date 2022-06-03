import sys
import numpy as np

def is_palin(s):
    i = 0
    while i < len(s) - i - 1:
        if s[i] != s[len(s)-i-1]:
            return False
        i += 1
    return True

def n_palin_recurse(s, i, j, k, cache):
    if i == 0: 
        if j == k-1 and is_palin(s[i: j+1]):
            cache[i][j] = 1
        else:
            cache[i][j] = 0
        return cache[i][j]
    if cache[i][j] != -1:
        return cache[i][j]
    subst = s[i:j+1]
    n_palin_recurse(s, i-1, j, k, cache)
    n_palin_recurse(s, i-1, j-1, k, cache)
    if is_palin(subst) and j-i >= k-1:
        n_palin_recurse(s, i-1, i-1, k, cache)
        cache[i][j] = max(
                cache[i-1][j],
                cache[i-1][j-1],
                cache[i-1][i-1] + 1
            )
    else:
        cache[i][j] = max(
                cache[i-1][j],
                cache[i-1][j-1]
            )

def n_palin(s, k):
    cache = [[-1 for i in range(len(s))] for j in range(len(s))]
    n_palin_recurse(s, len(s)-1, len(s)-1, k, cache)
    return cache[len(s)-1][len(s)-1]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: python {argv[0]} <string> <k>")
    print(n_palin(sys.argv[1], int(sys.argv[2])))
    # print(np.array(cache))
