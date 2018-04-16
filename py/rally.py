# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

from lib import *
from col import *

def same(x): return x

def csv(file):
  with open(file) as fs:
    for line in fs:
      line = re.sub(r'([\n\r\t]|#.*)', "", line)
      row  = [z.strip() for z in line.split(",")]
      if len(row)> 0:
        yield row

def using(src, use = None):
  for row in src:
    use = use or [n for n,x in enumerate(row) 
                  if x[0] is not THE.ignore]
    yield [row[n] for n in use]

def nways(src,ts):
  prob = (len(ts) - 1) / len(ts)
  for m,row in enumerate(using(src)):
    for t in ts:
      t.header(row)
      if m > 0:
        row = [col.add(cell) for col,cell in zip(t.cols,row)] 
        fun = t.train if r() < prob else t.test
        fun(row) 

def rows(i):
  for row in meta(i):
    yield [col.discretize(cell) for col,cell in zip(cols,row)]

class Every:
  def __init__(i, most=THE.era, action=same): 
    i.n, i._action, i.cache, i.most = 0, action, [], most
  def __add__(i,x):
    i.cache += [x]
    if len(i.cache) >= i.most: 
      i.action()
  def action(i):
    i.n += 1
    random.shuffle(i.cache)
    if i.cache: i._action(i.n, i.cache)
    i.cache = []

def watch(pred, actual, row, goals, bores=None, abcds=None):
  abcds = abcds or {g:Abcd(g) for g in goals}
  bores = bores or {g:Bore(g) for g in goals}
  for g in goals:
    abcds[g].update( pred,actual )
    bores[g].update( actual,row )
  return bores,abcds

class Abcd:
  def __init__(i, goal):
    i.goal = goal
    i.a,i.b,i.c,i.d = 0,0,0,0
  def update(i, pred, actual):
    """    | false | true
    silent |   a   |  b
      loud |   c   |  d   """
    if pred == i.goal: # then loud
      if actual == i.goal: i.d += 1 
      else: i.c += 1
    else: # then silent
      if actual == i.goal: i.b += 1
      else: 
        i.a += 1
  def report(i):
    z = 10**-32
    a,b,c,d = i.a, i.b, i.c, i.d
    return o(a=a,b=b,c=c,d=d,
             acc  = (a+d) / (a+b+c+d + z),
             pd   =     d / (b+d     + z),
             pf   =     c / (a+c     + z),
             prec =     d / (c+d     + z))

class Bore:
  def __init__(i, goal):
    i.best, i.rest = {},{}
    i.bests = i.rests =0 
    i.goal  = goal
  def update(i,actual,row):
    if actual == i.goal: 
      i.bests += 1
    else: 
      i.rests += 1
    for m,cell in enumerate(row):
      what = i.best if actual == i.goal else i.rest
      what[(m,cell)] = what.get((m,cell), 0) + 1
  def ranges(i):
    z = -10**32
    all = []
    for m,cell in i.best:
      b    = i.best[(m,cell)]       / (i.bests + z)
      r    = i.rest.get((m,cell),0) / (i.rests + z)
      br   = b**b/(b+r+z)
      all += [(br,m,cell)]
    return sorted(all, reverse=False)

class Table(Pretty):
  def __init__(i,n,label=""):
    i.n,i.label = n,label
    i._setup = False
  def header(i, names):
    if not i._setup:
      i._setup  = True
      i.setup(names)
  def setup(i, names):
      i.tests   = []
      i.abcd    = []
      i.every   = Every(action=i.row)
      i.names   = names
      i.cols    = [Col(n,name) for n,name 
                   in enumerate(i.names)]
      i.x, i.y  = [], []
      for n,name in enumerate(names):
        what  = i.y if name[0] == THE.klass else i.x
        what += [n]
  def test(i,  row): pass #out('.'); i.tests += [row]
  def train(i, row): i.every + row
  def row(i,m,rows): 
    if i.n == 0:
      for row in rows:
        print([int(x) for x in row])
        print([col.discretize(cell) for cell,col 
             in zip(row,i.cols)])

def file2Tables(f,n):
  ts = [Table(n,label='[%s] %s ' % (n,f)) 
        for n in range(n)] 
  nways( csv(f), ts )
  return ts

#for row in ranges(Table(file="../data/china.csv")): print(row)
rseed()
file2Tables("../data/china.csv", 3)

def _abcd1():
  a,b,c="a","b","c"
  goals = [a,b,c]
  bores, abcds = None, None
  for pred,actual in ([[a,a],[b,b],[b,b],
                      [b,b],[c,c],[b,b],[c,c]]):
    bores,abcds = watch(pred,actual,[], goals,bores,abcds)
  for g  in goals:
    print(g, abcds[g].report())

def _abcd2():
  a,b,c="a","b","c"
  goals = [a,b,c]
  bores, abcds = None, None
  for actual,pred in ((a,a),(a,a),(a,a),(b,a),(b,a),(c,a),
                      (a,b),(a,b),(a,b),(a,b),(a,b),(b,b),
                      (b,b),(b,b),(b,b),(b,b),(b,b),(c,b),
                      (a,c),(a,c),(b,c),(b,c),(c,c),(c,c),
                      (c,c),(c,c),(c,c),(c,c),(c,c),(c,c)):
    bores,abcds = watch(pred,actual,[], goals,bores,abcds)
  for g  in goals:
    print(g, abcds[g].report())

#_abcd2()

"""
              a b c == actual
  predicted a 1 0 0
            b 0 4 0
            c 0 0 2
  ]]--
  _abcd([[ a a b b b b b b c c b b c c  ]])
  
  --[[
              a b c == actual
  predicted a 3 2 1
            b 5 6 1
            c 2 2 8
  ]]--
  _abcd([[   a a a a a a
                  b a b a
                  c a 
                  a b a b a b a b a b
                  b b b b b b b b b b b b
                  c b
                  a c a c
                  b c b c
                  c c c c c c c c 
                  c c c c c c c c 
             ]])
   --[[
              a b c == actual
  predicted a 1 1 0
            b 1 1 1
            c 0 1 1
  ]]--
  _abcd([[ a a b a a b b b c b b c c c  ]])
"""

