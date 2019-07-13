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

import unittest
from big_collatz_fast import shortcut
from random import randrange

#assumes that tuple_naive is right
class TestTuples(unittest.TestCase):

    def test_tuple8(self):
        n = randrange(1, 256)
        self.assertEqual(shortcut._tuple8(n), shortcut._tuple_naive(n, 8))

    def test_tuple64(self):
        n = randrange(256, 1 << 64)
        self.assertEqual(shortcut._tuple64(n), shortcut._tuple_naive(n, 64))

    def test_tuple_recursive(self):
        blocks = randrange(2, 10)
        n = randrange(1, 1 << (blocks * 64))
        self.assertEqual(shortcut._tuple_recursive(n, blocks), shortcut._tuple_naive(n, blocks * 64))

    def test_tuple_acceler8ed(self):
        steps = randrange(8, 64)
        n = randrange(1, 1 << (steps + 1))
        self.assertEqual(shortcut._tuple_acceler8ed(n, steps), shortcut._tuple_naive(n, steps))

    def test_tuple_general(self):
        steps = randrange(8, 64) * 64
        n = randrange(1, 1 << (steps + 1))
        self.assertEqual(shortcut._tuple_general(n, steps), shortcut._tuple_naive(n, steps))

class TestCount(unittest.TestCase):
    #as with the tuples test, this involves comparison against the naive algorithm.
    def test_count_small(self):
        n = randrange(1, 256)
        self.assertEqual(shortcut._count(n), shortcut._small_count(n))

    def test_count_small_2(self):
        n = randrange(256, 65536)
        self.assertEqual(shortcut._count(n), shortcut._small_count(n))

    def test_count_medium(self):
        n = randrange(65536, 1 << 128)
        self.assertEqual(shortcut._count(n), shortcut._small_count(n))

    def test_count_large(self):
        n = randrange(1 << 128, 1 << (128 + randrange(0, 1024)))
        self.assertEqual(shortcut._count(n), shortcut._small_count(n))

class TestJump(unittest.TestCase):
    pass

unittest.main()
