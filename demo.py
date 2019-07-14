##   Copyright 2019 Brian Quach
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

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

##print_timings((1 << 20000) - 1)

#function examples
"""
big_collatz_fast.ordinary.count_steps(n)

big_collatz_fast.shortcut.count_steps(n)
big_collatz_fast.shortcut.jump(n, steps)

big_collatz_fast.odds.count_steps(n)
"""
