#!/usr/bin/env python
import dev
import unittest
import pyprimesieve
from itertools import izip_longest, dropwhile
try:
    from numpy import ones, bool, r_, nonzero, ndarray, allclose
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def _primes_numpy(n):
    """
    Input n>=6, Returns a array of primes, 2 <= p < n
    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """
    sieve = ones(n/3 + (n%6==2), dtype=bool)
    for i in xrange(1,int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k/3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)/3::2*k] = False
    return r_[2,3,((3*nonzero(sieve)[0][1:]+1)|1)]


def _primes(n):
    """
    Input n>=6, Returns a list of primes, 2 <= p < n
    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        sieve[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-correction) if sieve[i]]


class TestPrimes(unittest.TestCase):
    def test_1(self):
        self.assertEqual(pyprimesieve.primes(1), [])

    def test_2(self):
        self.assertEqual(pyprimesieve.primes(2), [])

    def test_3(self):
        self.assertEqual(pyprimesieve.primes(3), [2])

    def test_4(self):
        self.assertEqual(pyprimesieve.primes(4), [2, 3])

    def test_prime_count_1(self):
        self.assertEqual(len(pyprimesieve.primes(10**7)), 664579)

    def test_prime_count_2(self):
        self.assertEqual(len(pyprimesieve.primes(10**8)), 5761455)

    #def test_prime_count_3(self):
    #    self.assertEqual(len(pyprimesieve.primes(10**9)), 50847534)

    def test_emptylist_1(self):
        self.assertEqual(pyprimesieve.primes(0), [])

    def test_emptylist_2(self):
        self.assertEqual(pyprimesieve.primes(-1), [])

    def test_ranges_1(self):
        # start > n
        self.assertEqual(pyprimesieve.primes(411, 42), [])

    def test_ranges_2(self):
        # start < 0 - should be uneffected as if it were 2
        self.assertTrue(sequences_equal(pyprimesieve.primes(-100, 42), primes(42)))

    def test_ranges_3(self):
        # arbitrary point to start
        self.assertTrue(sequences_equal(pyprimesieve.primes(1412, 85747),
                                        dropwhile(lambda n: n < 1412, primes(85747))))

    def test_ranges_4(self):
        # arbitrary point to start
        self.assertTrue(sequences_equal(pyprimesieve.primes(74651, 975145),
                                        dropwhile(lambda n: n < 74651, primes(975145))))


def sequences_equal(lst1, lst2):
    return all(a == b for a, b in izip_longest(lst1, lst2))

primes = _primes_numpy if HAS_NUMPY else _primes

for i, n in enumerate(xrange(100, 10000, 100)):  # create sequence comparison tests for sieves of size n in range
    test = lambda self: self.assertTrue(sequences_equal(pyprimesieve.primes(n), primes(n)))
    setattr(TestPrimes, 'test_' + str(i), test)


if __name__ == "__main__":
    unittest.main()
