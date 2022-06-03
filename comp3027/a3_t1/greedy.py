import numpy as np
from itertools import product
import math

def get_arr(path):
    arr = []
    with open(path, "r") as f:
        for line in f.readlines():
            arr.append(list(map(float, line.split())))
    return arr

def is_proper(D):
    k = len(D)
    for i in range(k):
        if not math.isclose(D[i].sum(), int(D[i].sum())):
            return False
    for j in range(k):
        if not math.isclose(D.sum(axis=0)[j], int(D.sum(axis=0)[j])):
            return False
    return True

def is_feasible(D, P):
    k = len(D)
    for i in range(k):
        for j in range(k):
            if not (P[i][j] == int(D[i][j]) or P[i][j] == int(D[i][j]+1)):
                return False
    for i in range(k):
        if not math.isclose(sum(D[i]), sum(P[i])):
            return False
    for j in range(k):
        if not math.isclose(D.sum(axis=0)[j], P.sum(axis=0)[j]):
            return False
    return True

def greedy(D):
    k = len(D)
    P = np.array([[0 for _ in range(k)] for _ in range(k)])
    for i in range(k):
        for j in range(k):
            if math.isclose(D[i][j], 0) or math.isclose(D[i][j], 1):
                P[i][j] = D[i][j]
            else:
                if np.greater(D[i].sum(), P[i].sum()) and np.greater(D.sum(axis=0)[j], P.sum(axis=0)[j]):
                    P[i][j] = 1
                else:
                    P[i][j] = 0
    return P

def find_counterexample():
    k = 3
    possible_vals = (0, 0.5, 1)
    possible_rows = product(possible_vals, repeat=3)
    possible_debts = list(product(possible_rows, repeat=3))
    for i in range(len(possible_debts)):
        D = np.array(possible_debts[i])
        if is_proper(D):
            P = greedy(D)
            if not is_feasible(D, P):
                print(f"---PERMUTATION {i}---")
                print("PROPER DEBT TABLE")
                print(D)
                print("NOT FEASIBLE PAYMENT")
                print(P)
                print("-----------------")

if __name__ == "__main__":
    # D = np.array(get_arr("debts.txt"))
    # P = greedy(D)
    find_counterexample()