# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

from lib import *
from col import *

def same(x): return x

def csv(file, doomed = r'([\n\r\t]|#.*)'):
  with open(file) as fs:
    for line in fs:
      line = re.sub(doomed, "", line)
      row  = [z.strip() for z in line.split(",")]
      if len(row)> 0:
        yield row

def using(src, use    = None, 
               size   = None,
               ignore = THE.ignore):
  for m,row in enumerate(src):
    size = size or len(row)
    assert len(row)== size, "row %s not of size %s" % (m, size)
    use = use or [n for n,x in enumerate(row) if x[0] is not ignore]
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
      else: i.a += 1
  def report(i):
    z = 10**-32
    a,b,c,d = i.a, i.b, i.c, i.d
    pd = d / (b+d + z)
    pf = c / (a+c + z)
    return o(a=a, b=b, c=c, d=d,
             goal = i.goal,
             n    = a+b+c+d,
             pd   = pd,
             pf   = pf,
             d2h  = ((1 - pd)**2 + (0-pf)**2)**0.5/(2**0.5),
             acc  = (a+d) / (a+b+c+d + z),
             prec =     d / (c+d     + z))

def bore(goal, klasses):
    best, rest, nbest, nrest = {},{},0,0
    counts0 = klasses[0].y.has.counts:
    for x in counts0:
      if x == goal: nbest  = counts0[x]
      else:         nrest += counts0[x]
    for k in klasses: # one per class
      for col in k.x: # XXX no need: read straight from counts?
        counts = col.has.counts
        for x in counts:
          key  = (col.pos,x)
          what = best if x == goal else rest
          what[key] = what.get(key,0) + counts[x]
    z = -10**32
    all = []
    for m,cell in best:
      b    = best[(m,cell)]       / (nbest + z)
      r    = rest.get((m,cell),0) / (nrest + z)
      if b > r:
        b2r  = b**b/(b+r+z)
        all += [(b2r,m,cell)]
    return sorted(all, reverse=False)

class Table(Pretty):
  def __init__(i,n, label="", names=[]):
    i.n,i.label = n,label
    i.names  = names
    i.cols   = [Col(n,name) for n,name in enumerate(i.names)]
    i.abcdes = {}
    i.x, i.y = [], []
    for name,cols in enumerate(names,cols):
      if name[0] == THE.klass: i.y =  col
      else: i.x += [cols]
  def kompress(i,row):
    [col + cell for col,cell in zip(i.cols,row)]
  def keep(i,row):
    i.kompress(row)
    i.rows += [row]

# XXXX need a way to talk to N tlearners >>

def file2Tables(f,n,learners=[]):
  ts = [Table(n,label='[%s] %s ' % (n,f),
                learners=learners) 
        for n in range(n)] 
  nways( csv(f), ts )
  return ts

class NaiveBayes(Pretty):
  def __init__(i,t):
    i.klasses={}
    i.t = t
  def train(i,row):
    k = row[i.t.y.pos] 
    if k not in i.klasses:
      i.klasses[k] = i.t.headers()
    klass = 
    for col in i.t.x:
  def test(i,  row): pass #out('.'); i.tests += [row]
  def train(i, row): 
    if i.n == 0:
      print([int(x) for x in row])
      print([col.discretize(cell) for cell,col 
             in zip(row,i.cols)])

#for row in ranges(Table(file="../data/china.csv")): print(row)
rseed()
file2Tables("../data/china.csv", 3,[NaiveBayes])

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

