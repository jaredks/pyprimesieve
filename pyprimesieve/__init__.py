#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyprimesieve: Many primes, very fast. Uses primesieve.
# Copyright: (c) 2013, Jared Suttles. All rights reserved.
# License: BSD, see LICENSE for details.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""
pyprimesieve: Many primes, very fast. Uses primesieve.
- - - - - - - - - - - - - - - - - - - - - - - - - - -

primes(n): List of prime numbers up to `n`.

primes(start, n): List of prime numbers from `start` up to `n`.

primes_sum(n [, threads]): The summation of prime numbers up to `n`. If `threads` is given, that many threads will
be created. If not, the optimal number of threads will be determined.

primes_sum(start, n [, threads]): The summation of prime numbers from `start` up to `n`. If `threads` is given,
that many threads will be created. If not, the optimal number of threads will be determined.

primes_nth(n): The nth prime number.

factorize(n): List of tuples in the form of (*prime*, *power*) for the prime factorization of `n`.


Copyright: (c) 2013, Jared Suttles. All rights reserved.
License: BSD, see LICENSE for details.

"""

from subprocess import Popen
from multiprocessing import cpu_count
from os import path
from math import log
try:
    from ._pyprimesieve import primes, factorize
except ImportError:
    pass

__all__ = __dir__ = ['primes', 'primes_sum', 'primes_nth', 'factorize']
__title__ = 'pyprimesieve'
__version__ = '0.1.0'
__author__ = 'Jared Suttles'
__license__ = 'BSD License'
__copyright__ = 'Copyright 2013 Jared Suttles'


def primes_sum(*args, **kwargs):
    """
    The summation of prime numbers from `start` up to `n`. If `threads` is given, that many threads will be created.
    If not, the optimal number of threads will be determined.
    """
    if not args:
        raise TypeError('primes_sum expected at least 1 arguments, got 0')
    if len(args) > 2:
        raise TypeError('function takes at most 2 arguments ({} given)'.format(len(args)))
    try:
        start, n = args[0], args[1]
    except IndexError:
        start, n = 0, args[0]
    try:
        start, n = int(start), int(n)
    except ValueError:
        raise TypeError('an integer is required')
    if start > n or n < 3:
        return 0
    if start < 2:
        start = 2
    if n < primes_sum.threshold:
        return sum(primes(start, n))
    threads = kwargs.get('threads')
    if threads is None:
        try:
            threads = cpu_count()
        except NotImplementedError:
            threads = 1
    elif threads < 1:
        threads = 1
    pyprimes_primes_sum = path.join(path.dirname(path.realpath(__file__)), 'pyprimesieve_sum')
    try:
        p = Popen([pyprimes_primes_sum, str(n), str(start), str(threads)], stdout=-1)
        return int(p.stdout.read())
    except OSError:
        return sum(primes(start, n))
primes_sum.threshold = 2500000


def primes_nth(n):
    """
    The Nth prime number.
    """
    if n < 1:
        raise ValueError('must provide a positive number')
    elif n < 6:
        return [2, 3, 5, 7, 11][n-1]
    return primes(int(n*log(n*log(n))))[n-1]
