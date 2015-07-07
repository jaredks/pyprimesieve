#!/usr/bin/env python

import unittest
import pyprimesieve


class TestSumPrimes(unittest.TestCase):
    def test_bignums_1(self):
        self.assertEqual(pyprimesieve.primes_sum(10**5), sum(pyprimesieve.primes(10**5)))

    def test_bignums_2(self):
        self.assertEqual(pyprimesieve.primes_sum(10**6), sum(pyprimesieve.primes(10**6)))

    def test_bignums_3(self):
        self.assertEqual(pyprimesieve.primes_sum(10**7), sum(pyprimesieve.primes(10**7)))

    def test_bignums_4(self):
        self.assertEqual(pyprimesieve.primes_sum(10**8), sum(pyprimesieve.primes(10**8)))

    def test_smallnums_1(self):
        self.assertEqual(pyprimesieve.primes_sum(0), 0)

    def test_smallnums_2(self):
        self.assertEqual(pyprimesieve.primes_sum(1), 0)

    def test_smallnums_3(self):
        self.assertEqual(pyprimesieve.primes_sum(2), 0)

    def test_smallnums_4(self):
        self.assertEqual(pyprimesieve.primes_sum(3), 2)

    def test_smallnums_5(self):
        self.assertEqual(pyprimesieve.primes_sum(4), 5)

    def test_negative_1(self):
        self.assertEqual(pyprimesieve.primes_sum(-1), 0)

    def test_negative_2(self):
        self.assertEqual(pyprimesieve.primes_sum(-949248), 0)

    def test_negative_3(self):
        self.assertEqual(pyprimesieve.primes_sum(-949248, -4848), 0)

    def test_ranges_1(self):
        s = pyprimesieve.primes_sum(3, 13)
        self.assertEqual(s, 26)
        self.assertEqual(s, sum(pyprimesieve.primes(13)[1:]))

    def test_ranges_2(self):
        s = pyprimesieve.primes_sum(7, 22)
        self.assertEqual(s, 67)
        self.assertEqual(s, sum(pyprimesieve.primes(22)[3:]))

    def test_ranges_3(self):
        '''start > n... please no seg fault!!1'''
        self.assertEqual(pyprimesieve.primes_sum(55, 22), 0)

if __name__ == "__main__":
    unittest.main()
