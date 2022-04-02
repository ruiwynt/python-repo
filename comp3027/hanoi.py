import sys
import json

def hanoi(n):
    tower = [[n-i for i in range(n)], [], []]
    hanoi_recurse(n, tower, 0, 2, 1)

def hanoi_recurse(n, tower, src, dest, temp):
    if n == 0:
        return

    hanoi_recurse(n-1, tower, src, temp, dest)
    num = tower[src].pop() 
    assert num == n
    tower[dest].append(num)
    hanoi_recurse(n-1, tower, temp, dest, src)
    print(tower)

if __name__ == "__main__":
    hanoi(int(sys.argv[1]))
