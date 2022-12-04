#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time

from aocd import lines  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data


def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]

def torangeset(l):
    l2 = l.split("-")
    st = int(l2[0])
    end = int(l2[1])
    rng = set([x for x in range(st,end+1)])
    return rng
    

data = [l.split(",") for l in lines]
data = [[torangeset(l1),torangeset(l2)] for (l1,l2) in data]
pp(data)

overlap = 0
overlap2 = 0
for (r1,r2) in data:
    rint = r1.intersection(r2)
    if len(rint) == len(r1) or len(rint) == len(r2):
        overlap+=1
    if len(rint) > 0:
        overlap2 += 1
print(overlap)
    
print(overlap2)
