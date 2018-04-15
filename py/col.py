# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */
from lib import *

def gbin(n,bins,mean,sd) :
  "Main driver: convert 'n' into one of x 'bins'."
  breaks = {
      2:                         [0],
      3:                  [-0.43,    0.43],
      4:                  [-0.67, 0, 0.67],
      5:            [-0.84,-0.25, 0, 0.25, 0.84],
      6:            [-0.97,-0.43, 0, 0.43, 0.97],
      7:      [-1.07,-0.57,-0.18, 0, 0.18, 0.57, 1.07],
      8:      [-1.15,-0.67,-0.32, 0, 0.32, 0.67, 1.15],
      9:[-1.22,-0.76,-0.43,-0.14,    0.14, 0.43, 0.76, 1.22],
     10:[-1.28,-0.84,-0.52,-0.25, 0, 0.25, 0.52, 0.84, 1.28] }
  def bin(val,breaks, ninf = -10*10) :
    before,last = ninf,0
    for i,now in enumerate(breaks) :
      if val > before and val <= now:
        return i
      before,last = now,i
    return last+1
  return bin((n - mean) / sd, breaks[bins])

class Col:
  def adds(i,lst,f):
    [i.add(x,f) for x in lst]
    return i
  def add(i,x,f):
    if x is not "?":
      i.n += 1
      x = f(x)
      i.add1(x)
      return x
      
class Sym:
  def __init__(i,inits=[]):
    i.fromString = lambda z:z
    i.most,i.mode, i.counts = 0,None,{}
    [i.add1(x) for x in inits]
  def add1(i,x):
    m = i.counts[x] = i.counts.get(x,0) + 1
    if m > i.most:
      i.most,i.mode = m,x
  def norm(i,x): return x

class Num(Col):
  bins= THE.bins
  @staticmethod
  def isa(x):
    try: return int(x),Num
    except:
      try: return float(x),Num
      except: x,Sym
  def __init__(i,inits=[],ako=float):
    i.n = i.m2 = i.mu = 0.0
    i.fromString = ako
    [i.add(x) for x in inits]
  def s(i): 
    return (i.m2/(i.n - 1))**0.5
  def addi1(i,x):
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
    

