#!/usr/bin/env python

import os
import sys
import numpy as np
import argparse

from gol.life import Life

def sensitive(n, max_iter):
  # initial state
  init_state = np.random.random_integers(0, high=1, size=(n,n))
  # randomized altered state
  altered_state = init_state.copy()
  rand_x = np.floor(np.random.random() * n)
  rand_y = np.floor(np.random.random() * n)
  altered_state[rand_x][rand_y] = 1 - altered_state[rand_x][rand_y]
  l0 = Life(n, init_state)
  l1 = Life(n, altered_state) 
  print init_state
  print altered_state
  
  _sum = 0.0
  for i in xrange(max_iter):
    l0.step()
    l1.step()
    _delta = float(np.sum(np.abs(l0.state-l1.state)))/(n**2)
    _sum += _delta
  _final = float(np.sum(np.abs(l0.state-l1.state)))/(n**2)
  return _sum/max_iter, _final

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', default=10, type=int)
  parser.add_argument('-i', default=100, type=int)
  args = parser.parse_args()

  sensi,final = sensitive(args.n, args.i)

  print 'Sensitiveness: %lf' % (sensi * args.n**2)
  print 'Normalized:    %lf' % sensi
