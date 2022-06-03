# Parse input
def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.readline().split()))

# Dynamic programming algo
def max_ascending(arr):
    L = [1]
    for i in range(1, len(arr)):
        if arr[i] > arr[i-1]:
            L.append(L[-1]+1)
        else:
            L.append(1)
    f = L.index(max(L))
    s = f
    while L[s] != 1:
        s -= 1
    return arr[s:f+1], s, f

if __name__ == "__main__":
    arr = get_arr("arr.txt")
    a, s, f = max_ascending(arr)
    print(f"Maximum Ascending Array: {a}")
    print(f"Start Index: {s}\t End Index: {f}")
