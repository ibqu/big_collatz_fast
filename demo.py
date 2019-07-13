import timeit

def total_stopping_time(n):
    #assume that n is a positive int
    n2 = n
    steps = 0
    while n2 != 1:
        #0 if even, 1 if odd
        if n2 & 1:
            n2 = 3 * n2 + 1
        else:
            n2 = n2 // 2
        steps += 1
    return steps

import big_collatz_fast
def fast_total_stopping_time(n):
    return big_collatz_fast.ordinary.count_steps(n)

def print_timings(n):
    print("Times")
    print(
        "total_stopping_time:",
        str(round(timeit.timeit(lambda: total_stopping_time(n), number = 1), 5))
        + "s")
    print(
        "fast_total_stopping_time:",
        str(round(timeit.timeit(lambda: fast_total_stopping_time(n), number = 1), 5))
        + "s")

#print_timings((1 << 20000) - 1)
