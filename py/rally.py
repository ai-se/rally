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
    use = use or [i for i,x in enumerate(row) 
                  if x[0] is not THE.ignore]
    yield [row[i] for i in use]

def meta(src, names=None, cols=None):
  for m,row in enumerate(using(src)):
    names = names or row
    col   = cols or [Col(i,name) for i,name in enumerate(names)]
    if m > 0:
      print("names",names,"cols",cols,"row",row)
      for col,cell in zip(cols,row):
        col.add(cell)
      yield cols,row
        

def ranges(src):
  for cols,row in meta(src):
      yield cols,row, [ col.discretize(cell) 
                         for col,cell in zip(cols,row)]


for _,_,row in ranges(csv("../data/china.csv")):
    print(row)


