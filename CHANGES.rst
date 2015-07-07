Changes
=======

0.1.6 (2015-07-07)
------------------

- Python 3 support
- No longer assume `g++` in `setup.py` but rather tries installing with OpenMP and retries if that fails


0.1.5 (2015-07-05)
------------------

- added to pypi


0.1.4 (2013-08-06)
------------------

- Parallel prime summation is now a class
    - Threads calling callback method are NOT synchronized so faster on large input
    - Updated README in bench to reflect new timings (small input is slightly worse but large is twice as fast)


0.1.3 (2013-08-05)
------------------

- Fixed compilation warnings
- extern "C"
- Added more information regarding installation to README; updated docstring


0.1.2 (2013-07-12)
------------------

- primes_nth uses callback class instead of creating any PyObjects in order to call primes
    - Caused a memory leak and was unnecessary


0.1.1 (2013-07-12)
------------------

- Distutils setup.py: got multithreaded summation compiling with OpenMP
    - Removed all code to manually compile executable
    - CC and CXX environment variables set to avoid clang (and other non-openmp compilers) use
- Replaced executable code with parallelized function in the actual extension
- Rewrote primes_sum and primes_nth Python functions in C++ and removed Python script completely


0.1.0 (2013-07-06)
------------------

- pyprimesieve initial
