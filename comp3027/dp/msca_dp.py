# Parse input
def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.readline().split()))

# Dynamic programming algo
def mcs(arr):
    current_sum = 0
    best_sum = 0
    best_start = 0
    best_end = 0
    for i in range(len(arr)):
        current_sum += arr[i]
        current_sum = max(0, current_sum)
        if current_sum >= best_sum:
            best_sum = current_sum
            best_end = i
        if current_sum == 0:
            best_start = i+1
    return arr[best_start:best_end+1], sum(arr[best_start:best_end+1])

if __name__ == "__main__":
    arr = get_arr("arr.txt")
    max_arr, max_sum = mcs(arr)
    print(f"Maximum-Sum Contiguous Subarray: {max_arr}")
    print(f"Sum: {max_sum}")
