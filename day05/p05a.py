#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time
import re 

from aocd import lines  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data


def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]

#pp(lines)
lns = [q for q in lines]

cols = None 
num_cols = 0
for l in lns:
    if '[' in l:
        if cols is None:
            llen = len(l)
            num_cols = int((llen+1)/4)
            print(f"num_cols: {num_cols}")
            cols = []
            for i in range(num_cols):
                cols.append([])
        for i in range(num_cols):
            ind = 1+(4*i)
            ch = l[ind]
            if ch != " ":
                cols[i] = [ch] + cols[i]
pp(cols)
        
pat = re.compile("move (\d+) from (\d+) to (\d+)")
for l in lns:
    if l.startswith("move"):
        m = pat.match(l)
        #print(m.groups())
        num = int(m.groups()[0])
        src = int(m.groups()[1])
        dst = int(m.groups()[2])
        print(f"move {num} from {src} to {dst}")
        for i in range(num):
            c = cols[src-1].pop()
            cols[dst-1].append(c)
        pp(cols)
        print()
res = ""
for c in cols:
    res += c[-1]
print(res)
