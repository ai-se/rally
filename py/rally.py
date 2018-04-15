# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

from lib import *
from col import *

def same(x): return x

def rows(file):
  with open(file) as fs:
    for line in fs:
      line = re.sub(r'([\n\r\t]|#.*)', "", line)
      row  = [z.strip() for z in line.split(",")]
      if len(row)> 0:
        yield row

def using(src, use = None):
  for row in src:
    use = use or [i for i,x in enumerate(lst) 
                  if x[0] == THE.ignore]
    yield [row[i] for i in use]

def cols(src, names=None, stats=None):
  for m,row in enumerate(using(src)):
    names = names or row
    stats = stats or [None for _ in row]
    if m > 0:
      for i,(name,stat,cell) in enumerate(zip(names,stats,row)):
        if cell is not THE.ignore:
          if cell==None:
            what = Num if Num.isa(cell) else Sym
            col  = cols[i] = what(name,i)
        yield cols,row
        
def stats(src):
  for cols,row in enumerate(cols(src)):
    for col,cell in zip(cols,row):
      col.add( col.fromString(cell) )

for x in rows("../data/china.csv"):
  print(x)

run()

