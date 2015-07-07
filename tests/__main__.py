#!/usr/bin/env python

import unittest
from test_primes import TestPrimes
from test_primes_sum import TestSumPrimes
from test_factorize import TestFactorize
from test_primes_nth import TestNthPrimes

suite = unittest.TestSuite()
suite.addTests([unittest.TestLoader().loadTestsFromTestCase(TestPrimes),
                unittest.TestLoader().loadTestsFromTestCase(TestSumPrimes),
                unittest.TestLoader().loadTestsFromTestCase(TestFactorize),
                unittest.TestLoader().loadTestsFromTestCase(TestNthPrimes)])

#runner = unittest.TextTestRunner()
#runner.run(suite)
unittest.TextTestRunner().run(suite)
