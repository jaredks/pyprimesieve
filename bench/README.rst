Sum of primes
-------------

Running on a MacBook Pro 2Ghz Intel Core i7, best of 12 runs. All times are in ms.

``primes_sum`` is the parallelized prime summation function provided in ``pyprimesieve``.

``sumofprimes`` is calling Python's built-in ``sum`` function on the list of primes generated by
``pyprimesieve.primes``.

.. code-block:: bash

    10**5
    primes_sum 0.0650882720947
    sumofprimes 0.276803970337

    10**6
    primes_sum 0.452995300293
    sumofprimes 2.51293182373

    10**7
    primes_sum 4.27412986755
    sumofprimes 23.059129715

    10**8
    primes_sum 12.6960277557
    sumofprimes 262.270927429


Primes
------

Benchmark each algorithm.

.. warning::
   Will not run on Python 3 as algorithms were copied from other's answers at `this discussion on SO`_ which may or may
   not be compatible.


.. _`this discussion on SO`: http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python
