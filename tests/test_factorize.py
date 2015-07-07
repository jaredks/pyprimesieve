#!/usr/bin/env python
import unittest
import pyprimesieve
from test_primes import sequences_equal
import random

try:
    xrange
except NameError:
    xrange = range


def factorize(n):
    """
    List of the prime factorization of the given number represented by tuples of the prime and power.
    """
    prime_factors = []
    if n < 2:
        return prime_factors
    i = 0
    while not n & 1:
        n //= 2
        i += 1
    if i > 0:
        prime_factors.append((2, i))
    for p in xrange(3, n, 2):  # use n here but won't ever be > int(sqrt(n))+1
        if p*p > n:
            break
        i = 0
        while n % p == 0:
            n //= p
            i += 1
        if i > 0:
            prime_factors.append((p, i))
    if n > 1:
        prime_factors.append((n, 1))
    return prime_factors


class TestFactorize(unittest.TestCase):
    def test_negative_1(self):
        self.assertEqual(pyprimesieve.factorize(-1), [])

    def test_negative_2(self):
        self.assertEqual(pyprimesieve.factorize(-48485), [])

l = list(range(10**6))
random.shuffle(l)
l = l[:10**4]
for i, n in enumerate(l):
    test = lambda self: self.assertTrue(sequences_equal(pyprimesieve.factorize(n), factorize(n)))
    setattr(TestFactorize, 'test_' + str(i), test)

if __name__ == "__main__":
    unittest.main()
