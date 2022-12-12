#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time
from copy import deepcopy
import math 
from util import *
import astar
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()
#lines = ex 


pp(lines)

def height(ch):
    if ch == "S":
        ch = "a"
    elif ch == "E":
        ch = "z"
    return ord(ch)-ord("a")

map = [[height(ch) for ch in row] for row in lines]
#pp(map)

possible_starts = []
start = None
end = None
for rowidx,row in enumerate(lines):
    for colidx,col in enumerate(row):
        if col == 'S':
            start = (rowidx,colidx)
            possible_starts.append((rowidx,colidx))
        elif col == 'E':
            end = (rowidx,colidx)
        elif col == 'a':
            possible_starts.append((rowidx,colidx))

def neighbors(pos):
    rowidx,colidx = pos 
    height = map[rowidx][colidx]
    nbrs = []
    if rowidx > 0:
        h = map[rowidx-1][colidx]
        if h <= (height+1):
            nbrs.append((rowidx-1,colidx))
    if (rowidx+1) < len(map):
        h = map[rowidx+1][colidx]
        if h <= (height+1):
            nbrs.append((rowidx+1,colidx))
    if colidx > 0:
        h = map[rowidx][colidx-1]
        if h <= (height+1):
            nbrs.append((rowidx,colidx-1))
    if (colidx+1) < len(map[0]):
        h = map[rowidx][colidx+1]
        if h <= (height+1):
            nbrs.append((rowidx,colidx+1))
    return nbrs

def distance(pos1,pos2):
    return 1

def cost(n,goal):
    return int(1 * (abs(n[0]-goal[0])+abs(n[1]-goal[1])))

shortest = math.inf
for st in possible_starts:
    try:
        path = list(astar.find_path(st,end,neighbors,heuristic_cost_estimate_fnct=cost))
        #pp(path) 
        steps = len(path)-1
        print(f"{st} ->  {steps}") # includes both the start and end, but number of steps only needs one
        if shortest > steps:
            shortest = steps
    except:
        print(f"failed on {st}")
print(f"shortest: {shortest}")
