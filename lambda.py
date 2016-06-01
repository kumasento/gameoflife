#!/usr/bin/env python
import os
import sys
import numpy as np

import argparse
from gol.life import Life

def lyapunov(n, max_iter):
  # l0 = Life(n, np.ones((n, n),dtype=np.int8))
  l0 = Life(n)
  _sum = 0
  for i in xrange(max_iter):
    _delta = l0.step()
    if _delta != 0:
      _sum += np.log(_delta)
  return _sum * 1.0/max_iter

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', default=10, type=int)
  parser.add_argument('-i', default=100, type=int)
  args = parser.parse_args()

  num_test = 100
  l_sum = 0.0
  ls = []
  for i in xrange(num_test):
    l = lyapunov(args.n, args.i)
    ls.append(l)
    print "TEST %3d: VAL %lf SUM %lf\t AVG %lf" % (i, l, np.sum(ls), np.average(ls))

  print '=> FINAL '
  print np.average(ls)
  print 'Variance:', np.var(ls)
