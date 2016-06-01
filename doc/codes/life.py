import numpy as np
from scipy import ndimage

class Life:

  def __init__(self, n):
    self.n = n
    # Conway's Game of Life is a 2D grids network
    self.state = np.random.random_integers(0, high=1, size=(n, n))
    # Weight
    self.w = np.array([[1,1,1],[1,10,1],[1,1,1]])

  def step(self):
    # initialize a new state
    self.state = ndimage.convolve(self.state, self.w, mode='wrap')
    self.state = np.int8(
        (self.state ==  3) | 
        (self.state == 12) | 
        (self.state == 13))
    
