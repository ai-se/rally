# /* vim: set tabstop=2 softtabstop=2 shiftwidth=2 expandtab : */

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
  help("run unit tests",                          tests     = False),
  #elp("tiles display width",                    tiles     = 40),
  #elp("small effect size (Cliff's dela)",       cliff     = [0.147, 0.33, 0.474]),
  help("keep at most, say, 128 samples",          samples   = [128,256,128,512,1024]),
  help("y-axis bins",                             bins      = [5,2,3,4,6,7,8,9,10]),
  help("in pretty print, round numbers",          round     = 3),
  help("random number seed",                      seed      = 61409389),
  help("ignore cells, cols characters",           ignore    = "?"),
  help("class character",                         klass     = "!"),
  help("training data (csv format)",              train     = "train.csv"),
  help("testing data (csv format)",               test      = "test.csv"),
  help("verbose print",                           verbose   = True),
  # --------------------------------------------------------------------
  # System
  help("Run some test function, then quit",       run       = "")
  ]


