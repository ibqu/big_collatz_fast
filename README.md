# big_collatz_fast
Want to examine the [Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture) for large numbers like 2<sup>10 000 000</sup> - 1, without spending hours waiting for results?
If so, this module will help you (If not, go away).

If it's even, halve it. If it's odd, triple it and add one ("3n + 1"). The Collatz Conjecture is the unproven conjecture that performing these steps on a positive number will always result in reaching 1.

The number of these steps is known as the "total stopping time".

It may be naively computed like this:
```
#demo.py
def total_stopping_time(n):
    #assume that n is a positive int
    n2 = n
    steps = 0
    while n2 != 1:
        #0 if even, 1 if odd
        if n2 & 1:
            n2 = 3n2 + 1
        else:
            n2 = n2 / 2
        steps += 1
    return steps
```

Or it may be quickly computed like this:
```
#demo.py
import big_collatz_fast
def fast_total_stopping_time(n):
    return big_collatz_fast.ordinary.count_steps(n)
```

The difference in their speed is obvious for large numbers.

```
>>> print_timings((1 << 20000) - 1)
Times
total_stopping_time: 4.88768s
fast_total_stopping_time: 0.12028s
```
## Main ideas
The obvious way of counting steps is shown above.

This can be sped up by a significant constant factor by using the "shortcut" sequence (described in the module functions section below), and using a [lookup table and precomputation to skip several shortcut steps at a time](https://en.wikipedia.org/wiki/Collatz_conjecture#Time%E2%80%93space_tradeoff).

This module constructs virtual lookup table entries recursively, in a way not found by a quick Google Scholar search. This avoids applying changes from small numbers of steps to the whole number each time. As the Karatsuba algorithm used by Python for large integer multiplication has a subquadratic time complexity, this module offers an asymptotic speedup (assuming that the Collatz Conjecture is correct)

## Module functions
### Ordinary sequence
As described above, this is where a step is done by halving the number if it is even, and tripling and adding 1 if it is odd.

This returns the total stopping time when counting the ordinary steps:
```
big_collatz_fast.ordinary.count_steps(n) #n is a positive integer
```
### Shortcut sequence
This is where even numbers are halved as normal, but odd numbers undergo a "(3n + 1) / 2" step.

This returns the total stopping time when counting the shortcut steps:
```
big_collatz_fast.shortcut.count_steps(n) #n is a positive integer
```

This jumps from `n` by `steps` shortcut steps, and returns the result:
```
big_collatz_fast.shortcut.jump(n, steps)
```

### Odds-only sequence
This is the sequence of odd numbers in the ordinary sequence.

This returns the total stopping time when counting the jumps between odd numbers:
```
big_collatz_fast.odds.count_steps(n)
```
## Possible improvements

- Optimise `big_collatz_fast.shortcut._tuple64` code and create more efficient equivalents for larger jumps
- Use a fast integer library for asymptotically faster multiplication
- Use a faster programming language
