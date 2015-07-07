#!/usr/bin/env python

import os
import sys
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


# the following code for C extension failure copied from SQLAlchemy's setup.py
# ----
ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)
if sys.platform == 'win32':
    # 2.6's distutils.msvc9compiler can raise an IOError when failing to
    # find the compiler
    ext_errors += (IOError,)


class BuildFailed(Exception):

    def __init__(self):
        self.cause = sys.exc_info()[1]  # work around py 2/3 different syntax


class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()
        except ValueError:
            # this can happen on Windows 64 bit, see Python issue 7511
            if "'path'" in str(sys.exc_info()[1]):  # works with both py 2/3
                raise BuildFailed()
            raise


def status_msgs(*msgs):
    print('*' * 75)
    for msg in msgs:
        print(msg)
    print('*' * 75)

# ----


with open('README.rst') as f:
    readme = f.read()

with open('CHANGES.rst') as f:
    changes = f.read()

PRIMESIEVE_DIR = 'primesieve/src'
PRIMESIEVE_FILES = ['EratBig.cpp', 'EratMedium.cpp', 'EratSmall.cpp', 'ParallelPrimeSieve.cpp', 'PreSieve.cpp',
                    'PrimeFinder.cpp', 'PrimeGenerator.cpp', 'PrimeSieve.cpp', 'SieveOfEratosthenes.cpp',
                    'WheelFactorization.cpp', 'popcount.cpp']
PRIMESIEVE = [os.path.join(PRIMESIEVE_DIR, filename) for filename in PRIMESIEVE_FILES]


def run_setup(openmp):
    if openmp:
        kwargs = {
            'extra_compile_args': ['-fopenmp'],
            'extra_link_args': ['-fopenmp']
        }
    else:
        kwargs = {}

    setup(
        name='pyprimesieve',
        version='0.1.6',
        description='Many primes, very fast. Uses primesieve.',
        author='Jared Suttles',
        url='https://github.com/jaredks/pyprimesieve',
        long_description=readme + '\n\n' + changes,
        license='BSD License',
        cmdclass={'build_ext': ve_build_ext},
        package_data={'': ['LICENSE']},
        ext_modules=[
            Extension('pyprimesieve', sources=['pyprimesieve/pyprimesieve.cpp'] + PRIMESIEVE,
                      include_dirs=[PRIMESIEVE_DIR], **kwargs),
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

try:
    run_setup(True)

except BuildFailed as exc:
    status_msgs(
        exc.cause,
        "WARNING: pyprimesieve could not be compiled using OpenMP flags.",
        "Failure information, if any, is above.",
        "Retrying the build without OpenMP support now."
    )

    run_setup(False)

    status_msgs(
        "WARNING: pyprimesieve could not be compiled using OpenMP.",
        "Function `primes_sum` will not execute in parallel on machines with multiple cores.",
        "Non-parallel build succeeded."
    )
