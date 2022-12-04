#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time

def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]

def priority(ch):
    o = ord(ch)
    if o <= ord('z') and o >= ord('a'):
        return o-ord('a')+1
    elif o <= ord('Z') and o >= ord('A'):
        return o-ord('A')+27
    else:
        print(f"ERROR!!! {ch} {o}")

with open("input.txt","r") as f:
  data = [(i[0:int(len(i)/2)],i[int(len(i)/2):]) for i in f.readlines()]

pp(data)
#for d in data[0][0]:
#    print(f"{d} -> {priority(d)}")
prisum = 0
for (rs1,rs2) in data:
    srs1 = set(rs1)
    srs2 = set(rs2)
    u = list(srs1.intersection(srs2))
    pri = priority(u[0])
    print(f"{rs1} {rs2} -- {u} {pri}")
    prisum += pri
print(prisum)
