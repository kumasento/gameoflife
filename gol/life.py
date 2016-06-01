
import numpy as np
from scipy import ndimage

class Life:

  def __init__(self, n, state=None):
    self.n = n
    # Conway's Game of Life is a 2D grids network
    if state is None:
      self.state = np.random.random_integers(0, high=1, size=(n, n))
    else:
      self.state = state
    # Weight
    self.w = np.array([[1,1,1],[1,10,1],[1,1,1]])
    self.state_list = [self.state]

  def step(self):
    # initialize a new state
    _state = ndimage.convolve(self.state, self.w, mode='constant')
    self.state = np.int8(
        (_state ==  3) | 
        (_state == 12) | 
        (_state == 13))
    self.state_list.append(self.state)
    
    _delta = self.state_list[-1]-self.state_list[-2]
    _delta = np.sum(abs(_delta))
    _delta = float(_delta)/(self.n)
    _delta += 1e-6
    return _delta
