#!/usr/bin/env python
import dev
from benchmark import benchmark
from subprocess import Popen, PIPE
from multiprocessing import cpu_count
from os import path
from pyprimesieve import primes


def sumofprimes(n):  # lambda expression is slower
    return sum(primes(n))


def primes_sum(n):  # reimplement lib function without smart selection
    threads = cpu_count()
    pyprimes_primes_sum = path.join(path.dirname(path.realpath(__file__)), '../pyprimesieve_sum')
    p = Popen([pyprimes_primes_sum, str(n), '0', str(threads)], stdout=PIPE)
    return int(p.stdout.read())


def main():
    for n in xrange(5, 9):
        print '10**{}'.format(n)
        n = 10**n
        print 'pyprimesieve.primes.sum', benchmark(primes_sum, n, bestof=12) * 10**3
        print 'sum(pyprimesieve.primes)', benchmark(sumofprimes, n, bestof=12) * 10**3
        print ''


if __name__ == "__main__":
    main()
