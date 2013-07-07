Prime sieve algorithm implemenations taken from [this discussion on SO][0].


Sum of primes
-------------

Running on a MacBook Pro 2Ghz Intel Core i7, best of 12 runs. All times are in ms. Calling built-in function sum on
the list returned from `pyprimesieve.primes` is faster for small values. As such, in the actual module, `pyprimesieve`
will use summation of the list at smaller input numbers.

    10**5
    pyprimesieve.primes.sum 7.57098197937
    sum(pyprimesieve.primes) 0.253915786743

    10**6
    pyprimesieve.primes.sum 7.84397125244
    sum(pyprimesieve.primes) 1.95789337158

    10**7
    pyprimesieve.primes.sum 11.45195961
    sum(pyprimesieve.primes) 22.7839946747

    10**8
    pyprimesieve.primes.sum 31.378030777
    sum(pyprimesieve.primes) 250.817060471


[0]: http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python
