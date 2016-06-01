
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot

from life import Life

class View:

  def __init__(self, life):
    self.fig = pyplot.figure()
    self.life = life
    pyplot.axis([0, life.n, 0, life.n])
    pyplot.xticks([])
    pyplot.yticks([])

    self.pic = None

  def update(self):
    if self.pic != None:
      self.pic.remove()

    self.pic = pyplot.pcolor(self.life.state, cmap=matplotlib.cm.gray_r)
    self.fig.canvas.draw()

  def animate(self, steps=10):
    self.steps = steps
    self.fig.canvas.manager.window.after(1000, self.animate_callback)
    pyplot.show()

  def animate_callback(self):
    for i in range(self.steps):
      self.life.step()
      self.update()
