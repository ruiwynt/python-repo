def get_arr(path):
    with open(path, "r") as f:
        return list(map(int, f.read().split()))

def reverse(arr):
    reverse_recurse(arr, len(arr)-1)

def reverse_recurse(arr, i):
    if i < 0:
        return
    arr.append(arr.pop(i))
    reverse_recurse(arr, i-1)

if __name__ == "__main__":
    arr = get_arr("arr.txt")
    print(arr)
    reverse(arr)
    print(arr)
