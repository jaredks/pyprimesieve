#!/usr/bin/env python

from __future__ import print_function

from timeit import Timer
from pyprimesieve import primes, primes_sum

def sumofprimes(n):  # lambda expression is slower
    return sum(primes(n))

if __name__ == "__main__":
    for n in range(5, 9):
        print('10**{}'.format(n))
        for fn in ['primes_sum', 'sumofprimes']:
            timer = Timer(stmt='{}({})'.format(fn, 10**n), setup='from __main__ import {}'.format(fn))
            timer = min(timer.repeat(repeat=12, number=1)) * 10**3
            print(fn, timer)
        print('')
