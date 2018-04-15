# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

from lib import *

def same(x): return x

def rows(file,prep=same):
  with open(file) as fs:
    for line in fs:
      line = re.sub(r'([\n\r\t]|#.*)', "", line)
      row = [z.strip() for z in line.split(",")]
      if len(row)> 0:
         yield prep(row) if prep else row

class Num:
  @staticcode
  def is(x):
    try: int(x)

  def __init__(i,inits=[]):
    i.n = i.m2 = i.mu = 0.0
    for x in inits: i + x
  def s(i): return (i.m2/(i.n - 1))**0.5
  def __add__(i,x):
    i.n   += 1
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)
  def tTestSame(i,j,conf=0.95):
    nom   = abs(i.mu - j.mu)
    s1,s2 = i.s(), j.s()
    denom = ((s1/i.n + s2/j.n)**0.5) if s1+s2 else 1
    df    = min(i.n - 1, j.n - 1)
    return  criticalValue(df, conf) >= nom/denom

def criticalValue(df,
  conf=0.95,
  xs= [             1,    2,     5,    10,    15,    20,    25,   30,    60,   100],
  ys= {0.9:  [ 3.078, 1.886, 1.476, 1.372, 1.341, 1.325, 1.316, 1.31,  1.296, 1.29],
       0.95: [ 6.314, 2.92,  2.015, 1.812, 1.753, 1.725, 1.708, 1.697, 1.671, 1.66],
       0.99: [31.821, 6.965, 3.365, 2.764, 2.602, 2.528, 2.485, 2.457, 2.39, 2.364]}):
  def interpolate(x,xs,ys):
    if x <= xs[0] : return ys[0]
    if x >= xs[-1]: return ys[-1]
    x0, y0 = xs[0], ys[0]
    for x1,y1 in zip(xs,ys):
      if x < x0 or x > xs[-1] or x0 <= x < x1:
        break
      x0, y0 = x1, y1
    gap = (x - x0)/(x1 - x0)
    return y0 + gap*(y1 - y0)
  #-------------------------- 
  return interpolate(df, xs, ys[conf])

def hedges(i,j,small=0.38):
  num   = (i.n - 1)*i.s**2 + (j.n - 1)*j.s**2
  denom = (i.n - 1) + (j.n - 1)
  sp    = ( num / denom )**0.5
  delta = abs(i.mu - j.mu) / sp
  c     = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
  return delta * c < small

class Col:
  def __init__(i):
    i.has = None
  def __add__(i,x):

for x in rows("../data/china.csv"):
  print(x)



run()

