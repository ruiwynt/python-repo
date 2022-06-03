from flow_digraph import FlowDigraph
from pprint import PrettyPrinter
from itertools import product
import sys
import numpy as np

def read_table(path):
    with open(path, "r") as f:
        return np.array([list(map(float, line.strip().split())) for line in f.readlines()])

def to_flow(D):
    """Reduction to Max Flow"""
    k = len(D)
    D = np.array(D)
    row_sums = D.sum(axis=1)
    col_sums = D.sum(axis=0)
    H = FlowDigraph()
    H.add_vertex("s")
    H.add_vertex("t")
    for i in range(k):
        H.add_vertex(f"u_{i+1}")
        H.add_edge("s", f"u_{i+1}", int(row_sums[i]))
    for j in range(k):
        H.add_vertex(f"v_{j+1}")
        H.add_edge(f"v_{j+1}", "t", int(col_sums[j]))
    for i in range(k):
        for j in range(k):
            if np.isclose(D[i][j], 1):
                if (("s", f"v_{j+1}")) not in H.capacities.keys():
                    H.add_edge("s", f"v_{j+1}", 1)
                else:
                    H.capacities[("s", f"v_{j+1}")] += 1
                H.capacities[("s", f"u_{i+1}")] -= 1
                H.add_edge(f"u_{i+1}", f"v_{j+1}", 0)
            elif not np.isclose(D[i][j], 0):
                H.add_edge(f"u_{i+1}", f"v_{j+1}", 1)
    H.max_flow()
    return H

def to_payment(D, H, k):
    """Transforming Max Flow to Payment Table"""
    P = np.zeros((k, k), dtype=np.int32)
    for i in range(k):
        for j in range(k):
            if D[i][j] == 0 or D[i][j] == 1:
                P[i][j] = D[i][j]
            else:
                P[i][j] = H.flows[(f"u_{i+1}", f"v_{j+1}")]
    return P

def is_proper(D):
    row_sums = D.sum(axis=0)
    for rs in row_sums:
        if not np.isclose(rs, int(rs)):
            return False
    col_sums = D.sum(axis=1)
    for cs in col_sums:
        if not np.isclose(cs, int(cs)):
            return False
    return True

def reduce(D):
    """Main reduction algorithm"""
    if not is_proper(D):
        print("D is not admissible (not proper)")
        sys.exit(0)
    H = to_flow(D)
    P = to_payment(D, H, len(D))
    return P

def satisfies_integrality(D, P):
    k = len(D)
    for i in range(k):
        for j in range(k):
            if np.isclose(D[i][j], 0) and P[i][j] == 1 or \
                    np.isclose(D[i][j], 1) and P[i][j] == 0:
                return False
    return True

def is_feasible(D, P):
    if not satisfies_integrality(D, P):
        print("VIOLATES INTEGRALITY")
        return False

    k = len(D)
    for i in range(k):
        for j in range(k):
            if not (P[i][j] == int(D[i][j]) or P[i][j] == int(D[i][j]+1)):
                return False
    for i in range(k):
        if not np.isclose(sum(D[i]), sum(P[i])):
            return False
    for j in range(k):
        if not np.isclose(D.sum(axis=0)[j], P.sum(axis=0)[j]):
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) == 1:
        possible_vals = (0, 0.5, 1)
        possible_rows = product(possible_vals, repeat=len(possible_vals))
        possible_debts = product(possible_rows, repeat=len(possible_vals))
        for D_perm in iter(possible_debts):
            D = np.array(D_perm)
            if is_proper(D):
                P = reduce(D)
                if not is_feasible(D, P):
                    print("----------------------------")
                    print("PROPER DEBT TABLE")
                    print(D)
                    print("FEASIBLE PAYMENT TABLE")
                    print(P)
                    print("----------------------------")
    elif len(sys.argv) == 2:
        D = read_table(sys.argv[1])
        print(D)
        print(reduce(D))
