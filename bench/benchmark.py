#!/usr/bin/env python
from time import time

def benchmark(func, *args, **kwargs):
    start, stop, bestof = kwargs.get('start', 0), kwargs.get('stop'), kwargs.get('bestof', 1)
    assert bestof > 0
    best_time = float('inf')
    for _ in xrange(bestof):
        start_time = time()
        if stop:
            for n in xrange(start, stop):
                func(n)
        else:
            func(*args)
        best_time = min(time() - start_time, best_time)
    return best_time
