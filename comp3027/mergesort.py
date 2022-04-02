# Parse input
def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.readline().split()))

# Divide and conquer algo
def merge_sort(arr):
    return mergesort_recurse(arr, 0, len(arr))

def mergesort_recurse(arr, start, end):
    # Start is inclusive, end is not inclusive.
    if end - start <= 1:
        return arr[start:end]
    
    mid = (start+end+1)//2
    # Split and delegate
    left = mergesort_recurse(arr, start, mid)
    right = mergesort_recurse(arr, mid, end)
    print(left, right)

    # Combine
    i = 0
    j = 0
    merged = []
    while i < len(left) or j < len(right):
        if i == len(left):
            merged.append(right[j])
            j += 1
        elif j == len(right):
            merged.append(left[i])
            i += 1
        elif right[j] < left[i]:
            merged.append(right[j])
            j += 1
        else:
            merged.append(left[i])
            i += 1
    return merged

if __name__ == "__main__":
    arr = get_arr("arr.txt")
    print(arr)
    arr_sorted = merge_sort(arr)
    print(arr_sorted)
