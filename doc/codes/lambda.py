def lyapunov(n, max_iter):
  l0 = Life(n)
  _sum = 0
  for i in xrange(max_iter):
    _delta = l0.step()
    if _delta != 0:
      _sum += np.log(_delta)
  return _sum * 1.0/max_iter
