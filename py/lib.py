# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

import sys,re,random,argparse,traceback,time,math,copy,pprint

def helps(): return [
"""
Rally: a challenging approach to data mining.
(C) 2018, tim@menzies.us UNLICENSE
This is free and unencumbered software released into the public domain.
""","""
"Give me the fruitful error any time, full of seeds, bursting with
its own corrections. You can keep your sterile truth for yourself."
-- Vilfredo Pareto

""",
  # sway
  help("run unit tests",                   tests   = False),
  #elp("tiles display width",              tiles   = 40),
  #elp("small effect size (Cliff's dela)", cliff   = [0.147, 0.33, 0.474]),
  help("keep at most, say, 128 samples",   samples = [128,256,128,512,1024]),
  help("y-axis bins",                      bins    = [5,2,3,4,6,7,8,9,10]),
  help("era size",                         era     = 10),
  help("in pretty print, round numbers",   round   = 3),
  help("random number seed",               seed    = 61409389),
  help("ignore cells, cols characters",    ignore  = "?"),
  help("class character",                  klass   = "!"),
  help("repeats",                          repeats = [5,10]),
  help("n-ways",                           nways   = [3,5,10]),
  help("training data (csv format)",       train   = "train.csv"),
  help("testing data (csv format)",        test    = "test.csv"),
  help("verbose print",                    verbose = True),
  # --------------------------------------------------------------------
  # System
  help("Run some test function, then quit",       run       = "")
  ]

def help(h, **d):
  def help1():
    if val is False :
      return dict(help=h, action="store_true")
    if isinstance(val,list):
      return dict(help=h, choices=val,default=default, metavar=m ,type=t)
    else:
      return dict(help=h + ("; e.g. %s" % val), default=default, metavar=m, type=t)
  key,val = list(d.items())[0]
  default = val[0] if isinstance(val,list) else val
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  return "--" + key, help1()

def options(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before,
              formatter_class = argparse.RawDescriptionHelpFormatter)
  for key, rest in lst:
    parser.add_argument(key,**rest)
  return parser.parse_args()

THE = options(*helps())

def ro(x)        : return round(x,THE.round)
def rseed(s=None): random.seed(s or THE.seed)
r = random.random

#--------------------------------------------------
def outln(*l):
  return out(*l, nl=True)

def out(*l,nl=None):
  if THE.verbose: 
    sys.stdout.write(" ".join(l))
    if nl:
      sys.stdout.write("\n")
    sys.stdout.flush()

#--------------------------------------------------
class unittest:
  PASS=FAIL=0
  @staticmethod
  def oks():
    if THE.tests:
      print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
            PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))
  @staticmethod
  def ok(f):
    if THE.tests:
      try:
        print("\n-----| %s |-----------------------" % f.__name__)
        if f.__doc__:
          print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
        f()
        print("# pass")
        PASS += 1
      except Exception as e:
        FAIL += 1
        print(traceback.format_exc())
    return f
 
ok = unittest.ok

def isa(x,y): return isinstance(x,y)

def kv(d, private="_"):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,THE.round) if isa(x,float) else x
  return '('+', '.join(['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]) + ')'

class Pretty(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)

class o(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)

def run():
  if THE.run:
    f= eval("lambda : %s()" %THE.run)
    ok(f())
    sys.exit()

