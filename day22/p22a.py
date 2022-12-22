#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
os.environ["COLUMNS"] = "220" # I usually keep my terminal around 240
from sys import exit
from collections import defaultdict,namedtuple
import time
from copy import deepcopy
import math 
import astar
import re

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".splitlines()
#lines = ex


dir = "R"
dirval = {"R":0, "D":1, "L":2,"U":3}

def turnright(dir):
    match dir:
        case "R":
            return "D"
        case "D":
            return "L"
        case "L":
            return "U"
        case "U":
            return "R"
        case other:
            print(f"ERROR: direction={dir}")

def turnleft(dir):
    match dir:
        case "R":
            return "U"
        case "D":
            return "R"
        case "L":
            return "D"
        case "U":
            return "L"
        case other:
            print(f"ERROR: direction={dir}")


pp(lines)

mapdata = []
instructionstr = ""

for l in lines:
    if len(l.strip()) == 0:
        pass
    elif "#" in l or "." in l:
        mapdata.append(l)
    else:
        instructionstr = l 
pp(mapdata)
pp(instructionstr)

pat = re.compile("(\d+|[RL])")

inst1 = pat.findall(instructionstr)
pp(inst1)

inst = []
for i in inst1:
    try:
        n = int(i)
        inst.append(n)
    except:
        inst.append(i)
print(inst)

mapwidth = max([len(row) for row in mapdata])
mapheight = len(mapdata)
print(f"mapheight={mapheight}, mapwidth={mapwidth}")

oldmd = mapdata
mapdata = []
for row in oldmd:
    while len(row) < mapwidth:
        row = row + " "
    mapdata.append(row)

pp(mapdata)

def getnextpos(mapdata,pos,dir):
    match dir:
        case "R":
            return ((pos[0]+1) % mapwidth, pos[1])
        case "D":
            return (pos[0], (pos[1]+1) % mapheight)
        case "L":
            if pos[0] == 0:
                return (mapwidth-1, pos[1])
            return (pos[0]-1, pos[1])
        case "U":
            if pos[1] == 0:
                return (pos[0], mapheight-1)
            return (pos[0], pos[1]-1 )
        case other:
            print(f"ERROR: direction={dir}")

def getnext(mapdata,pos,dir):
    dta = " "
    peekpos = pos
    while dta == " ":
        peekpos = getnextpos(mapdata,peekpos,dir)
        dta = mapdata[peekpos[1]][peekpos[0]]
        print(f"{peekpos}:{dta} ",end="")
    print
    return peekpos,dta


def doinst(inst,mapdata,pos=None,dir=None):
    if pos is None or dir is None:
        for x,ch in enumerate(mapdata[0]):
            if ch == ".":
                pos = (x,0)
                dir = "R"
                break
        print(f"[{pos} {dir}]")
    ins = inst.pop(0)
    if type(ins) == int: # step count
        for s in range(ins):
            newpos,val = getnext(mapdata,pos,dir)
            if val == "#":
                break # wall is next
            pos = newpos
    else:
        if ins == "L":
            dir = turnleft(dir)
        elif ins == "R":
            dir = turnright(dir)
        else:
            print(f"ERROR: dir {dir}")
    print(f"ins={ins} -> {pos} {dir}")
    return pos,dir

pos = None 
while len(inst) > 0:
    pos,dir = doinst(inst,mapdata,pos,dir)
val = (1000 * (pos[1]+1)) + (4 * (pos[0]+1)) + dirval[dir]
print(val)