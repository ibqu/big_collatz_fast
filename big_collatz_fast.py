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

class _Misc():
    def __init__(self):
        def jump_with_tuple(n, atuple):
            return (n >> atuple[3]) * atuple[1] + atuple[0]

        def last_bits(n, bits):
            return n & ((1 << bits) - 1)

        #this is just for shortening
        def combine_into_tuple(n, atuple1, atuple2):
            return (n, atuple1[1] * atuple2[1], atuple1[2] + atuple2[2], atuple1[3] + atuple2[3])

        self.jump_with_tuple = jump_with_tuple
        self.last_bits = last_bits
        self.combine_into_tuple = combine_into_tuple

class _Shortcut():
    def __init__(self):
        #unpack _misc
        global _misc
        jump_with_tuple = _misc.jump_with_tuple
        last_bits = _misc.last_bits
        combine_into_tuple = _misc.combine_into_tuple
        
        def lookup_table(bits):
            return tuple(tuple_naive(n, bits) for n in range(1 << bits))

        def tuple_naive(n, steps):
            #format: (add, multiply, odds, bits)
            #mnemonic: AMOB / AMOS
            n2 = last_bits(n, steps)
            multiply = 1
            odds = 0
            for i in range(steps):
                #odd case
                if n2 & 1:
                    n2 = (n2 * 3) + 1
                    multiply *= 3
                    odds += 1
                n2 >>= 1
            return (n2, multiply, odds, steps)

        def tuple8(n):
            return table8[n & 255]

        def tuple64(n):
            multiply = 1
            odds = 0
            n2 = n & ((1 << 64) - 1)
            for i in range(8):
                atuple = tuple8(n2)
                n2 = jump_with_tuple(n2, atuple)
                multiply *= atuple[1]
                odds += atuple[2]
            return (n2, multiply, odds, 64)

        #here 'blocks' are groups of 64 bits
        def tuple_recursive(n, blocks):
            #base case
            if blocks == 1: return tuple64(n)

            lesserBlocks = blocks >> 1
            greaterBlocks = blocks - lesserBlocks

            n2 = last_bits(n, blocks * 64)

            atuple1 = tuple_recursive(n2, lesserBlocks)
            n2 = jump_with_tuple(n2, atuple1)
            atuple2 = tuple_recursive(n2, greaterBlocks)
            n2 = jump_with_tuple(n2, atuple2)

            return combine_into_tuple(n2, atuple1, atuple2)

        def tuple_acceler8ed(n, steps):
            #reduce the tuple creation overhead
            if steps <= 16: return tuple_naive(n, steps)
            
            multiply = 1
            odds = 0
            n2 = last_bits(n, steps)

            #do jumping using the lookup table
            for i in range(steps // 8):
                atuple = tuple8(n2)
                n2 = jump_with_tuple(n2, atuple)
                multiply *= atuple[1]
                odds += atuple[2]

            #deal with the remainder
            minor_tuple = tuple_naive(n2, steps & 7)
            n2 = jump_with_tuple(n2, minor_tuple)
            multiply *= minor_tuple[1]
            odds += minor_tuple[2]

            return (n2, multiply, odds, steps)

        def tuple_general(n, steps):
            if steps < 128: return tuple_acceler8ed(n, steps)
            #split it into subproblems
            #solvable using this procedure in addition to tuple_recursive

            lesserBlocks = steps // 128
            greaterBits = (steps - lesserBlocks * 64)
            
            n2 = last_bits(n, steps)

            atuple1 = tuple_recursive(n2, lesserBlocks)
            n2 = jump_with_tuple(n2, atuple1)
            atuple2 = tuple_general(n2, greaterBits)
            n2 = jump_with_tuple(n2, atuple2)
            
            return combine_into_tuple(n2, atuple1, atuple2)

        def small_count(n):
            #for tiny integers (flexible but not efficient)
            odds = 0
            steps = 0
            n2 = n
            while n2 != 1:
                if n2 & 1:
                    odds += 1
                    n2 = ((n2 * 3) + 1)
                n2 >>= 1
                steps += 1
            return (odds, steps)

        def medium_count(n):
            #for somewhat larger numbers
            odds = 0
            steps = 0
            n2 = n
            while n2.bit_length() > 8:
                atuple = tuple8(n2)
                n2 = jump_with_tuple(n2, atuple)
                odds += atuple[2]
                steps += 8
            small_count_results = small_count(n2)
            #premature optimisation is evil
            odds += small_count_results[0]
            steps += small_count_results[1]
            return (odds, steps)

        def large_count(n):
            odds = 0
            steps = 0
            n2 = n
            while n2.bit_length() > 128:
                #skip a number of steps approximately equal to half the bit length
                atuple = tuple_recursive(n2, n2.bit_length() // 128)
                n2 = jump_with_tuple(n2, atuple)
                odds += atuple[2]
                steps += atuple[3]
            medium_count_results = medium_count(n2)
            #premature optimisation is evil
            odds += medium_count_results[0]
            steps += medium_count_results[1]
            return (odds, steps)

        #need error checking
        def count(n):
            if type(n) != int:
                raise TypeError("Non-int given to shortcut.count")
            if n < 1:
                raise ValueError("Non-positive number given to shortcut.count")
            return large_count(n)

        def count_steps(n):
            if type(n) != int:
                raise TypeError("Non-int given to shortcut.count_steps")
            if n < 1:
                raise ValueError("Non-positive number given to shortcut.count_steps")
            return count(n)[1]

        def jump(n, steps):
            if type(n) != int:
                raise TypeError("Non-int given to shortcut.count")
            return jump_with_tuple(n, tuple_general(n, steps))

        table8 = lookup_table(8)

        #export private
        self._lookup_table = lookup_table
        self._tuple_naive = tuple_naive
        self._tuple8 = tuple8
        self._tuple64 = tuple64
        self._tuple_recursive = tuple_recursive
        self._tuple_acceler8ed = tuple_acceler8ed
        self._tuple_general = tuple_general
        self._small_count = small_count
        self._medium_count = medium_count
        self._large_count = large_count

        #export public
        self._count = count
        self.count_steps = count_steps
        self.jump = jump

class _Ordinary():
    def __init__(self):
        global shortcut
        count = shortcut._count
        def count_steps(n):
            if type(n) != int:
                raise TypeError("Non-int given to ordinary.count_steps")
            if n < 1:
                raise ValueError("Non-positive number given to ordinary.count_steps")
            c = count(n)
            return c[0] + c[1]
        self.count_steps = count_steps

class _Odds():
    def __init__(self):
        global shortcut
        count = shortcut._count
        def count_steps(n):
            if type(n) != int:
                raise TypeError("Non-int given to odds.count_steps")
            if n < 1:
                raise ValueError("Non-positive number given to odds.count_steps")
            return count(n)[0]

_misc = _Misc()
shortcut = _Shortcut()
ordinary = _Ordinary()
odds = _Odds()
