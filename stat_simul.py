from multiprocessing import Pool
import random
import time
import sys

def play_game(x, y, p):
    """True if x wins else False"""
    x_score = x
    y_score = y
    turns = 0
    threshold = 100*p
    while x_score != 0 and y_score != 0:
        roll = random.randint(1, 100)
        if roll <= threshold:
            x_score += 1
            y_score -= 1
        else:
            x_score -= 1
            y_score += 1
        turns += 1
    return (True, turns) if x_score != 0 else (False, turns)

def print_results(turns, x_wins, N):
    print(f"AVERAGE TURNS: {turns/N}")
    print(f"X WON {x_wins} GAMES")
    print(f"P(X WINS): {x_wins/N}")
    print(f"Y WON {N-x_wins} GAMES")
    print(f"P(Y WINS): {(N-x_wins)/N}")

def run_multiprocess(x, y, p, N):
    print(f"SIMULATING GAME MULTIPROCESSING WITH X = {x}, Y = {y}, p = {p}")
    with Pool(processes=None) as pool:
        vals = [pool.apply_async(play_game, (x, y, p)) for i in range(N)]
        pool.close()
        pool.join()
    total_turns = 0
    x_wins = 0
    for i in range(N):
        vals[i] = vals[i].get()
        if vals[i][0] is True:
            x_wins += 1
        total_turns += vals[i][1]
    print_results(total_turns, x_wins, N)

def run_single(x, y, p, N):
    total_turns = 0
    x_wins = 0
    print(f"SIMULATING GAME SINGLE PROCESS WITH X = {x}, Y = {y}, p = {p}")
    for i in range(N):
        result, turns = play_game(x, y, p)
        total_turns += turns
        if result is True:
            x_wins += 1
    print_results(total_turns, x_wins, N)

def time_wrap(f):
    def f_wrapped(*args):
        start = time.time()
        results = f(*args)
        finish = time.time()
        print(f"{f.__name__} took {round(finish-start, 6)} seconds to run.")
        print("")
        return results
    return f_wrapped


def main(x, y, p, N):
    # time_wrap(run_single)(x, y, p, N)
    time_wrap(run_multiprocess)(x, y, p, N)

X = 100
Y = 150
p = 0.5

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        N = int(sys.argv[1])
    if len(sys.argv) >= 4:
        X = int(sys.argv[2])
        Y = int(sys.argv[3])
    if len(sys.argv) >= 5:
        p = float(sys.argv[4])
    main(X, Y, p, N)
