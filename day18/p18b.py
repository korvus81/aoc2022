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


ex = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines()

#lines = ex 

#pp(lines)

coords = [[int(x) for x in c.split(",")] for c in lines]
#pp(coords)

# 6 sides on a cube
# 1,1,1 and 2,1,1 are connected because they are off by 1....
# when two cubes are connected, they each lose one side

sides_if_none_connected = len(coords) * 6

maxx,maxy,maxz = coords[0]
minx,miny,minz = coords[0]


sides_lost_to_touching = 0
for ci1, c1 in enumerate(coords):
    x1,y1,z1 = c1
    if x1 < minx:
        minx = x1
    if y1 < miny:
        miny = y1 
    if z1 < minz:
        minz = z1

    if x1 > maxx:
        maxx = x1
    if y1 > maxy:
        maxy = y1 
    if z1 > maxz:
        maxz = z1

    for ci2 in range(ci1+1,len(coords)):
        c2 = coords[ci2]
        
        x2,y2,z2 = c2
        if x1==x2 and y1==y2 and abs(z1-z2) == 1:
            sides_lost_to_touching += 2
        if x1==x2 and z1==z2 and abs(y1-y2) == 1:
            sides_lost_to_touching += 2
        if z1==z2 and y1==y2 and abs(x1-x2) == 1:
            sides_lost_to_touching += 2
print(f"sides starting: {sides_if_none_connected}, sides lost: {sides_lost_to_touching}, surface area: {sides_if_none_connected-sides_lost_to_touching}")
print(f"coord range: {minx}-{maxx}, {miny}-{maxy}, {minz}-{maxz}")

blocks = make3dList(" ",maxx+2,maxy+2,maxz+2)
for x,y,z in coords:
    blocks[x][y][z] = "#"

ext_surface_count = 0
for x in range(maxx+2):
    for y in range(maxy+2):
        if blocks[x][y][0] == " ":
            blocks[x][y][0] = "." # steam
        if blocks[x][y][maxz+1] == " ":
            blocks[x][y][maxz+1] = "." # steam

        if blocks[x][y][0] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at
        if blocks[x][y][maxz+1] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at

for x in range(maxx+2):
    for z in range(maxz+2):
        if blocks[x][0][z] == " ":
            blocks[x][0][z] = "." # steam
        if blocks[x][maxy+1][z] == " ":
            blocks[x][maxy+1][z] = "." # steam

        if blocks[x][0][z] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at
        if blocks[x][maxy+1][z] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at

for y in range(maxy+2):
    for z in range(maxz+2):
        if blocks[0][y][z] == " ":
            blocks[0][y][z] = "." # steam
        if blocks[maxx+1][y][z] == " ":
            blocks[maxx+1][y][z] = "." # steam

        if blocks[0][y][z] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at
        if blocks[maxx+1][y][z] == "#":
            ext_surface_count += 1 # this has a face we aren't looking at

count = 0
changed = True
while changed:
    print(f"Loop starting, count={count}")
    changed = False 
    for x in range(maxx+2):
        for y in range(maxy+2):
            for z in range(maxz+2):
                cur = blocks[x][y][z]
                if cur == ".": # if steam, try to expand
                    for offset in ((0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)):
                        xo= x+offset[0]
                        yo= y+offset[1]
                        zo= z+offset[2]
                        try:
                            peek = blocks[xo][yo][zo]
                            if xo == 2 and yo == 2 and zo == 5:
                                print(x,y,z)
                                print(peek)
                            if peek == " ":
                                blocks[xo][yo][zo] = "."
                                changed = True
                        except:
                            pass
    count += 1

surface = 0
internal_blocks = 0
for x in range(maxx+2):
    for y in range(maxy+2):
        for z in range(maxz+2):
            cur = blocks[x][y][z]
            if cur == " ":
                internal_blocks += 1
            if cur == ".": # if steam, see what I'm touching
                for offset in ((0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)):
                    xo= x+offset[0]
                    yo= y+offset[1]
                    zo= z+offset[2]
                    try:
                        peek = blocks[xo][yo][zo]
                        if peek == "#":
                            surface += 1
                    except:
                        pass
for b in blocks:
    for row in b:
        print("".join(row))
    print()

print(f"surface={surface}, ext_surface={ext_surface_count}, internal_blocks={internal_blocks}, total:{surface+ext_surface_count}")
print(f"legacy surface area: {sides_if_none_connected-sides_lost_to_touching}, minus internal: {sides_if_none_connected-sides_lost_to_touching-(internal_blocks*6)}")