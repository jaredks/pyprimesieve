pyprimesieve
============

Many primes, very fast. Uses primesieve_.

primesieve, one of the fastest (if not the fastest) prime sieve implementaions available, is actively maintained by
Kim Walisch.

It uses a segmented sieve of Eratosthenes with wheel factorization for a complexity of ``O(nloglogn)`` operations.


Performance
-----------

Regarding primesieve for C++:

    primesieve generates the first 50,847,534 primes up to 10^9 in just 0.4 seconds on a single core of an Intel Core
    i7-920 2.66GHz, this is about 50 times faster than an ordinary C/C++ sieve of Eratosthenes implementation and about
    10,000 times faster than trial-division. primesieve outperforms [Kim's] older ecprime_ (fastest from 2002 to 2010) by
    about 30 percent and also substantially outperforms primegen_ the fastest sieve of Atkin implementation on the
    web.

For comparison, on an Intel Core i7 2GHz, ``pyprimesieve`` populates an entire Python list of the first
50,847,534 primes in 1.40 seconds. It's expected that a Python implementation would be slower than C++ but,
surprisingly, by only one second.

``pyprimesieve`` outperforms all of the fastest prime sieving implementations for Python.

Time (ms) to generate the all primes below one million and iterate over them in Python:

===================  =============
     algorithm           time
-------------------  -------------
pyprimesieve         2.79903411865
primesfrom2to        13.1568908691
primesfrom3to        13.5800838470
ambi_sieve           16.1600112915
rwh_primes2          38.7749671936
rwh_primes1          48.5658645630
rwh_primes           52.0040988922
sieve_wheel_30       59.3869686127
sieveOfEratosthenes  59.4990253448
ambi_sieve_plain     161.740064621
sieveOfAtkin         232.724905014
sundaram3            251.194953918
===================  =============

It can be seen here that ``pyprimesieve`` is *4.7 times faster* than the fastest Python alternative using ``Numpy`` and
*13.85 times faster* than the fastest pure Python sieve.

All benchmark scripts and algorithms are available for reproduction. Prime sieve algorithm implementations were taken
from `this discussion on SO`_.

Functions
---------

**primes(n)**: List of prime numbers up to `n`.

**primes(start, n)**: List of prime numbers from `start` up to `n`.

**primes_sum(n)**: The summation of prime numbers up to `n`. The optimal number of threads will be determined for the
given number and system.

**primes_sum(start, n)**: The summation of prime numbers from `start` up to `n`. The optimal number of threads will be
determined for the given numbers and system.

**primes_nth(n)**: The nth prime number.

**factorize(n)**: List of tuples in the form of (prime, power) for the prime factorization of `n`.


Installation
------------

.. code-block:: bash

    pip install pyprimesieve

**NOTE**: To enable the parallelized version of prime summation, you must use a compiler that supports OpenMP. You may
need to pass a valid compiler as an environment variable.


Testing
-------

After installation, you can make sure everything is working by running the following inside the project root folder,

.. code-block:: bash

    python tests


License
-------

"Modified BSD License". See LICENSE for details. Copyright Jared Suttles, 2015.

.. _primesieve: https://github.com/kimwalisch/primesieve
.. _ecprime: http://primzahlen.de/referenten/Kim_Walisch/index2.htm
.. _primegen: http://cr.yp.to/primegen.html
.. _`this discussion on SO`: http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python
