#!/usr/bin/env python
import dev
import unittest
import pyprimesieve


class TestNthPrimes(unittest.TestCase):
    def test_smallnums_1(self):
        self.assertEqual(pyprimesieve.primes_nth(1), 2)

    def test_smallnums_2(self):
        self.assertEqual(pyprimesieve.primes_nth(4), 7)

    def test_bignums_1(self):
        self.assertEqual(pyprimesieve.primes_nth(10001), 104743)

    def test_bignums_2(self):
        self.assertEqual(pyprimesieve.primes_nth(94949), 1228567)

    def test_bignums_3(self):
        self.assertEqual(pyprimesieve.primes_nth(81749371), 1648727417)

    def test_exception_1(self):
        with self.assertRaises(ValueError):
            pyprimesieve.primes_nth(0)

    def test_exception_2(self):
        with self.assertRaises(ValueError):
            pyprimesieve.primes_nth(-1111)

if __name__ == "__main__":
    unittest.main()
