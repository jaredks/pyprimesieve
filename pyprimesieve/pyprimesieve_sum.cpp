/*
  pyprimesieve: Many primes, very fast. Uses primesieve.
  Copyright: (c) 2013, Jared Suttles. All rights reserved.
  License: BSD, see LICENSE for details.
*/
#include <iostream>
#include "../primesieve/src/ParallelPrimeSieve.h"

uint64_t sum = 0;

void summation(uint64_t prime) {
    sum += prime;
}

int main(int argc, char* argv[]){
    uint64_t n       = (uint64_t) strtoul(argv[1], NULL, 10)-1;
    uint64_t start   = (uint64_t) strtoul(argv[2], NULL, 10);
    char     threads = atoi(argv[3]);

    ParallelPrimeSieve pps;
    pps.setNumThreads(threads);
    pps.generatePrimes(start, n, summation);
    std::cout << sum;
    return 0;
}
