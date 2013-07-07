#!/usr/bin/env python
import unittest
from test_primes import TestPrimes
from test_sum_primes import TestSumPrimes
from test_factorize import TestFactorize

suite = unittest.TestSuite()
suite.addTests([unittest.TestLoader().loadTestsFromTestCase(TestPrimes),
                unittest.TestLoader().loadTestsFromTestCase(TestSumPrimes),
                unittest.TestLoader().loadTestsFromTestCase(TestFactorize)])

#runner = unittest.TextTestRunner()
#runner.run(suite)
unittest.TextTestRunner().run(suite)
