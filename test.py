#!/usr/bin/env python

import os
import sys

import math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import argparse
import time

from gol.life import Life
from gol.view import View

from multiprocessing import Process,Lock,Manager

def is_state_equal(s1, s2):
  return np.sum(s1 == s2) == (s1.shape[0]*s1.shape[1])

def find_cycle(life, verbose=False):
  max_iter = len(life.state_list)
  max_cycle = int(math.floor(max_iter * 0.5))
  # iterate cycle number
  for d in np.arange(1, max_cycle):
    # search from backward
    is_cycle = True
    for t in np.arange(1, d+1):
      s1 = life.state_list[-t]
      s2 = life.state_list[-(t+d)]
      if not is_state_equal(s1, s2):
        is_cycle = False
        break
    if is_cycle == True:
      return d
  return -1

def draw(life, num_cycle):
  num_y = min(num_cycle, 3)
  num_x = int(math.ceil(float(num_cycle)/num_y))
  plt.figure(1, (num_y*(life.n+1),num_x*(life.n+1))) 
  for i in range(num_cycle):
    sub = plt.subplot(num_x,num_y,i+1)
    sub.axis([0, life.n, 0, life.n])
    sub.pcolor(life.state_list[-num_cycle+i], cmap=matplotlib.cm.gray_r)
  plt.savefig('img_%d_%d.png' % (life.n,num_cycle))

def test(start_idx, end_idx, lock, cycle_dict):
  for i in xrange(start_idx,end_idx):
    # print "Testing case: %d ..." % i
    init_state = np.zeros((n, n), dtype=np.int8)
    for x in xrange(n):
      for y in xrange(n):
        init_state[x][y] = np.int8((i >> (x*n+y)) & 1)

    life = Life(n, init_state)
    for t in np.arange(max_iter):
      life.step()
      
    cycle = find_cycle(life)
    lock.acquire()
    if cycle_dict.has_key(cycle):
      cycle_dict[cycle] += 1
    else:
      if cycle >= 2:
        draw(life, cycle)
      cycle_dict[cycle] = 1
    lock.release()

if __name__ == '__main__':

  parser = argparse.ArgumentParser(
      prog='test',
      description='Game of life test program',
      epilog='Test and make statistics')
  parser.add_argument('-n', default=3, type=int, help='N is the width of map')
  parser.add_argument('-p', default=1, type=int, help='Number of threadings')
  parser.add_argument('-i', default=100, type=int, help='Number of iterations')
  args = parser.parse_args()

  n = args.n 
  max_iter = args.i
  end_idx = 2**(n*n)

  num_thread = args.p
  workload = int(math.ceil(float(end_idx)/num_thread))
  print 'Processes: %d' % num_thread
  print 'Workload:  %d' % workload
  print ''

  manager = Manager()
  cycle_dict = manager.dict()
  ps = []
  lock = Lock()
  start_idx = 0
  for t in range(num_thread):
    lower,upper = start_idx, min(end_idx,start_idx+workload)
    print 'Process %3d: [%8d, %8d]' % (t,lower,upper)
    ps.append(Process(target=test, args=(lower,upper,lock,cycle_dict)))
    start_idx = upper 
  print ''

  t1 = time.time()
  for p in ps:
    p.start()
  print '=> STARTED'
  print 'It will take about %lf seconds' % (workload * 0.01)
  for p in ps:
    p.join()
  print '=> JOINED'
  t2 = time.time()

  print 'Took %lf s' % ((t2-t1) * 1.0)
  print ''
  
  for k,v in cycle_dict.items():
    print 'Number of cycle %3d: %8d times' % (k,v)
