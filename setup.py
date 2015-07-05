#!/usr/bin/env python

import os
from distutils.core import setup, Extension

if 'CC' not in os.environ:
    os.environ['CC'] = 'g++'

if 'CXX' not in os.environ:
    os.environ['CXX'] = 'g++'

with open('README.md') as f:
    readme = f.read()

with open('CHANGES') as f:
    changes = f.read()

PRIMESIEVE_DIR = 'primesieve/src'
PRIMESIEVE_FILES = ['EratBig.cpp', 'EratMedium.cpp', 'EratSmall.cpp', 'ParallelPrimeSieve.cpp', 'PreSieve.cpp',
                    'PrimeFinder.cpp', 'PrimeGenerator.cpp', 'PrimeSieve.cpp', 'SieveOfEratosthenes.cpp',
                    'WheelFactorization.cpp', 'popcount.cpp']
PRIMESIEVE = [os.path.join(PRIMESIEVE_DIR, filename) for filename in PRIMESIEVE_FILES]

setup(
    name='pyprimesieve',
    version='0.1.4',
    description='Many primes, very fast. Uses primesieve.',
    author='Jared Suttles',
    url='https://github.com/jaredks/pyprimesieve',
    long_description=readme + '\n\n' + changes,
    license='BSD License',
    package_data={'': ['LICENSE']},
    ext_modules=[
        Extension('pyprimesieve', sources=['pyprimesieve/pyprimesieve.cpp'] + PRIMESIEVE,
                  include_dirs=[PRIMESIEVE_DIR], extra_compile_args=['-fopenmp'], extra_link_args=['-fopenmp']),
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
