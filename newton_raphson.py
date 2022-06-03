import sys
import numpy as np
from scipy.optimize import newton


def my_impl(mu, initial, maxiter):
    def nr_iterate(f, f_dash, x, maxiter):
        i = 0
        while i < maxiter:
            x = x - f(x)/f_dash(x)
            i += 1
        return x
    f = lambda x: np.exp(mu*(x-1)) - x
    f_dash = lambda x: mu*np.exp(mu*(x-1)) - 1
    return nr_iterate(f, f_dash, initial, maxiter)


def scipy_impl(mu, initial, maxiter):
    f = lambda x: np.exp(mu*(x-1)) - x
    return newton(f, initial, maxiter=maxiter)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("command line argument should be <mu> <x_initial> <iterations>")
        sys.exit(1)
    mu = float(sys.argv[1])
    initial  = float(sys.argv[2])
    maxiter = int(sys.argv[3])

    import timeit
    print(timeit.timeit("my_impl(mu, initial, maxiter)", globals=globals(), number = 10000))
    print(timeit.timeit("scipy_impl(mu, initial, maxiter)", globals=globals(), number = 10000))
