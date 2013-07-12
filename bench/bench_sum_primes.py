#!/usr/bin/env python
import dev
from benchmark import benchmark
from pyprimesieve import primes, primes_sum

def sumofprimes(n):  # lambda expression is slower
    return sum(primes(n))

if __name__ == "__main__":
    for n in xrange(5, 9):
        print '10**{}'.format(n)
        n = 10**n
        print 'pyprimesieve.primes.sum', benchmark(primes_sum, n, bestof=12) * 10**3
        print 'sum(pyprimesieve.primes)', benchmark(sumofprimes, n, bestof=12) * 10**3
        print ''
