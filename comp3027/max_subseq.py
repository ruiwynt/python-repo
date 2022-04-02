# Parse input
def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.read().split()))

# Backtracking Algo
cache = {}
n_calls = 0
n_cache_calls = 0

def max_asc_subseq(arr, cache_results):
    return max_asc_subseq_recurse(arr, 0, [], cache_results)

def max_asc_subseq_recurse(arr, i, chosen, cache_results):
    global n_calls
    global n_cache_calls
    if str((i, chosen)) in cache.keys() and cache_results is True:
        n_cache_calls += 1
        return cache[str((i, chosen))].copy()
    n_calls += 1
    if i == len(arr):
        return chosen
    dont_include = max_asc_subseq_recurse(arr, i+1, chosen, cache_results)
    if len(chosen) == 0 or chosen[-1] <= arr[i]:
        include = max_asc_subseq_recurse(arr, i+1, chosen + [arr[i]], cache_results)
        best = include if len(include) >= len(dont_include) else dont_include
        if cache_results is True:
            cache[str((i, chosen))] = best
        return best
    if cache_results is True:
        cache[str((i, chosen))] = dont_include
    return dont_include

if __name__ == "__main__":
    arr = get_arr("arr1.txt")
    subseq = max_asc_subseq(arr, False)
    print(f"RECURSING WITH NO MEMOISATION")
    print(f"Maximum Ascending Subsequence: {subseq}")
    print(f"Times Recursed: {n_calls}")
    print(f"Times Cache Called: {n_cache_calls}")
    print("")

    n_calls = 0
    subseq = max_asc_subseq(arr, True)
    print(f"RECURSING WITH MEMOISATION")
    print(f"Maximum Ascending Subsequence: {subseq}")
    print(f"Times Recursed: {n_calls}")
    print(f"Times Cache Called: {n_cache_calls}")
