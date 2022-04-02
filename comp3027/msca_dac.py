# Parse input
def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.readline().split()))    

# Divide and conquer algo
def mcs(arr):
    start, end = mcs_recurse(arr, 0, len(arr))
    return arr[start:end], sum(arr[start:end])

def mcs_recurse(arr, start, end):
    if end - start <= 0:
        return start, start
    if end - start == 1:
        if arr[start] > 0:
            return start, end
        else:
            return start, start
    
    left_s, left_e = mcs_recurse(arr, start, (start+end)//2)
    right_s, right_e = mcs_recurse(arr, (start+end)//2, end)

    left_sum = sum(arr[left_s:left_e])
    right_sum = sum(arr[right_s:right_e])
    combined_sum = sum(arr[left_s:right_e])

    if left_sum > right_sum and left_sum > combined_sum:
        return left_s, left_e
    elif right_sum > left_sum and right_sum > combined_sum:
        return right_s, right_e
    else:
        return left_s, right_e

if __name__ == "__main__":
    arr = get_arr("arr.txt")
    max_arr, max_sum = mcs(arr)
    print(f"Maximum-Sum Contiguous Subarray: {max_arr}")
    print(f"Sum: {max_sum}")
