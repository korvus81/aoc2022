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

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data



lines = list(lns)
ex = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".splitlines()

#lines = ex

pp(lines)

# have to have 500,0
minx = 500
maxx = 500
miny = 0
maxy = 0

paths = []
for ln in lines:
    path = []
    coords = ln.split("->")
    for c in coords:
        xs,ys = c.strip().split(",")
        x = int(xs)
        y = int(ys)
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x 
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
        path.append((x,y))
    paths.append(path)
pp(paths)
print(f"{minx}-{maxx}  {miny}-{maxy}")
floory = maxy + 2
maxy = floory 
if minx > (500-floory-1):
    minx = 500-floory-1

if maxx < (500+floory+1):
    maxx = 500+floory+1

scan = make2dList(".",maxx-minx+1,maxy-miny+1)

def printScan(scan):
    for row in scan:
        print("".join(row))
    print()

def getScanAt(x,y):
    if y == floory:
        return "#"
    return scan[y-miny][x-minx]

def updateScanAt(x,y,val):
    print(f"  ({x},{y})={val}")
    scan[y-miny][x-minx] = val

printScan(scan)
updateScanAt(500,0,"+")
printScan(scan)

for path in paths:
    startx,starty = path[0]
    updateScanAt(startx,starty,"#")
    curx = startx 
    cury = starty
    for destx,desty in path[1:]:
        print(f"curx={curx},cury={cury}  destx={destx},desty={desty}")
        while curx != destx or cury != desty:
            if curx > destx:
                curx -= 1
            elif curx < destx:
                curx += 1
            if cury > desty:
                cury -= 1
            elif cury < desty:
                cury += 1
            updateScanAt(curx,cury,"#")

printScan(scan)

def dropSand(scan):
    sandx = 500
    sandy = 0
    while True: #sandy < floory-1: # if we get to the end of this, we are going into the void
        if sandy == floory-1: # can't go lower, so stop here
            updateScanAt(sandx,sandy,"o")
            return False # not void yet
        elif getScanAt(sandx,sandy+1) == ".":
            sandy += 1
        elif getScanAt(sandx-1,sandy+1) == ".":
            sandy += 1
            sandx -= 1
        elif getScanAt(sandx+1,sandy+1) == ".":
            sandy += 1
            sandx += 1
        else: # nowhere to go!
            if sandx == 500 and sandy == 0:
                updateScanAt(sandx,sandy,"o")
                return True # blocking the opening!
            updateScanAt(sandx,sandy,"o")
            return False # not void yet
        
    return True # into the void!

units = 0
while not dropSand(scan):
    units += 1
    if units % 100 == 0:
        printScan(scan)
units += 1
printScan(scan)
print(units)