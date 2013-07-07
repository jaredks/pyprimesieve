#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils import sysconfig
from os import path
from subprocess import call
import sys
import shutil
import pyprimesieve

################################################################################
## Might have to adjust the following in the case of compile failure
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
COMPILERS_SUPPORTING_OPENMP = ['g++', 'gcc']
SUMMATION_COMPILE_OPTIONS = ['-fopenmp', '-lstdc++', '-O3']
################################################################################


PRIMESIEVE_DIR = 'primesieve/src'
PRIMESIEVE_FILES = ['EratBig.cpp', 'EratMedium.cpp', 'EratSmall.cpp', 'ParallelPrimeSieve.cpp', 'PreSieve.cpp',
                    'PrimeFinder.cpp', 'PrimeGenerator.cpp', 'PrimeSieve.cpp', 'SieveOfEratosthenes.cpp',
                    'WheelFactorization.cpp', 'popcount.cpp']
PRIMESIEVE = [path.join(PRIMESIEVE_DIR, filename) for filename in PRIMESIEVE_FILES]
PYPRIMESIEVE_SUM = 'pyprimesieve_sum'

setup(
    name='pyprimesieve',
    version=pyprimesieve.__version__,
    description='Many primes, very fast. Uses primesieve.',
    author='Jared Suttles',
    url='https://github.com/jaredks/pyprimesieve',
    long_description=open('README.md').read(),
    license='BSD License',
    package_data={'': ['LICENSE']},
    packages=['pyprimesieve'],
    ext_modules=[
        Extension('pyprimesieve._pyprimesieve', sources=['pyprimesieve/pyprimesieve.cpp'] + PRIMESIEVE,
                  include_dirs=[PRIMESIEVE_DIR]),
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


# pyprimesieve_sum
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def compile_prime_sum(x):
    compilecommand = ([x, '-o', PYPRIMESIEVE_SUM, 'pyprimesieve/pyprimesieve_sum.cpp'] +
                      SUMMATION_COMPILE_OPTIONS + PRIMESIEVE)
    print '\ncompiling {}\n'.format(PYPRIMESIEVE_SUM)
    print ' '.join(compilecommand), '\n'
    return call(compilecommand)

if all(compile_prime_sum(c) != 0 for c in COMPILERS_SUPPORTING_OPENMP):
    sys.exit('failed: could not compile {}'.format(PYPRIMESIEVE_SUM))
else:
    print 'successfully compiled {}'.format(PYPRIMESIEVE_SUM)
summation_path_from = path.join(path.dirname(path.realpath(__file__)), PYPRIMESIEVE_SUM)
summation_path_to = path.join(sysconfig.get_python_lib(), 'pyprimesieve/{}'.format(PYPRIMESIEVE_SUM))
print 'moving {} -> {}'.format(summation_path_from, summation_path_to)
shutil.move(summation_path_from, summation_path_to)
