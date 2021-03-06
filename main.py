#!/usr/bin/env python

import sys
import os
import argparse
import time

from gol.life import Life 
from gol.view import View

def run(n, step):
  print 'Running Game of Life ...'
  print 'Shape: %d X %d' % (n, n)
  print ''

  life = Life(n)
  view = View(life)
  view.animate(step)

if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(
      prog='gol',
      description='Game of Life implementation',
      epilog='A general purpose GoL implemenation. Mainly for my term paper')
  parser.add_argument('-n', default=10, type=int, help='width of the world') 
  parser.add_argument('-s', default=10, type=int, help='number of steps') 
  args = parser.parse_args()

  run(args.n, args.s)
