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




cube = [
    [row[50:100] for row in mapdata[0:50]], # front
    [row[100:150] for row in mapdata[0:50]], # right
    [row[50:100] for row in mapdata[50:100]], # bottom
    [row[50:100] for row in mapdata[100:150]], # back (should I flip this?)
    [row[0:50] for row in mapdata[100:150]], # left
    [row[0:50] for row in mapdata[150:200]], # top
]

pp(cube)


nextstep = {}

# front -- "top" edge to top face
for x in range(50,100):
    y = 0
    nextstep[((x,y),"U")] = ((0,150+(x-50)),"R")

# front -- "left" edge to left face
for y in range(0,50):
    x = 50
    nextstep[((x,y),"L")] = ((0,149-y),"R")

# front right and bottom should be ok


# right -- "bottom" edge to bottom face
for x in range(100,150):
    y = 49
    nextstep[((x,y),"D")] = ((99,50+(x-100)),"L")

# right -- "top" edge to top face
for x in range(100,150):
    y = 0
    nextstep[((x,y),"U")] = ((x-100,199),"U")

# right -- "right" edge to back face
for y in range(0,50):
    x = 149
    nextstep[((x,y),"R")] = ((99,149-y),"L")

# right left edge should be ok

# bottom -- "right" edge to right face 
for y in range(50,100):
    x = 99
    nextstep[((x,y),"R")] = ((y+50,49),"U")

# bottom -- "left" edge to left face
for y in range(50,100):
    x = 50
    nextstep[((x,y),"L")] = ((y-50,100),"D")

# bottom top and bottom edge should be ok

# back -- "right" edge to right face
for y in range(100,150):
    x = 99
    nextstep[((x,y),"R")] = ((149,49-(y-100)),"L")

# back -- "bottom" edge to top face
for x in range(50,100):
    y = 149
    nextstep[((x,y),"D")] = ((49,100+x),"L")

# back left and top edges should be ok

# left -- "top" edge to bottom face
for x in range(0,50):
    y = 100
    nextstep[((x,y),"U")] = ((50,50+x),"R")

# left -- "left" edge to front face 
for y in range(100,150):
    x = 0
    nextstep[((x,y),"L")] = ((50,49-(y-100)),"R")

# left right and bottom edges should be ok

# top -- "left" edge to front face
for y in range(150,200):
    x = 0
    nextstep[((x,y),"L")] = ((y-100,0),"D")

# top -- "bottom" edge to "top" edge of right face
for x in range(0,50):
    y = 199
    nextstep[((x,y),"D")] = ((x+100,0),"D")

# top -- "right" edge to "bottom" edge of back face
for y in range(150,200):
    x = 49
    nextstep[((x,y),"R")] = ((y-100,149),"U")


# top top edge should be ok

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
    # handle cube edges
    if (pos,dir) in nextstep:
        return nextstep[(pos,dir)]
    match dir:
        case "R":
            return ((pos[0]+1) % mapwidth, pos[1]),dir
        case "D":
            return (pos[0], (pos[1]+1) % mapheight),dir
        case "L":
            if pos[0] == 0:
                return (mapwidth-1, pos[1]),dir
            return (pos[0]-1, pos[1]),dir
        case "U":
            if pos[1] == 0:
                return (pos[0], mapheight-1),dir
            return (pos[0], pos[1]-1 ),dir
        case other:
            print(f"ERROR: direction={dir}")

def getnext(mapdata,pos,dir):
    dta = " "
    peekpos = pos
    while dta == " ":
        # we get dir back because it can change if we cross an edge
        peekpos,dir = getnextpos(mapdata,peekpos,dir)
        dta = mapdata[peekpos[1]][peekpos[0]]
        if dta == " ":
            print("ERROR?")
            time.sleep(1)
        print(f"{peekpos}:'{dta}'[{dir}] ",end="")
    print
    return peekpos,dta,dir


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
            newpos,val,maybedir = getnext(mapdata,pos,dir)
            if val == "#":
                break # wall is next
            dir = maybedir # only change direction if we actually move that step
            pos = newpos
            path.append((pos,dir))
    else:
        if ins == "L":
            dir = turnleft(dir)
        elif ins == "R":
            dir = turnright(dir)
        else:
            print(f"ERROR: dir {dir}")
    print(f"ins={ins} -> {pos} {dir}")
    return pos,dir




path = []

def printmap(mapdata,path):
    veryrecentlocs = {}
    recentlocs = {}
    locs = {}
    for pa in path[-1000:]:
        locs[pa[0]] = pa[1]
    for pa in path[-100:]:
        recentlocs[pa[0]] = pa[1]
    for pa in path[-10:]:
        veryrecentlocs[pa[0]] = pa[1]
    for y,row in enumerate(mapdata):
        for x,ch in enumerate(row):
            pos = (x,y)
            if pos in veryrecentlocs:
                p(f"[red]{locs[pos]}[/red]",end="")
            elif pos in recentlocs:
                p(f"[cyan]{locs[pos]}[/cyan]",end="")
            elif pos in locs:
                p(f"[green]{locs[pos]}[/green]",end="")
            else:
                p(ch,end="")
        print()
    print()

cnt = 0
pos = None 

#### FOR TESTING ####
#mapdata = [row.replace("#",".") for row in mapdata]
#inst = [10,"R",10,"L",50,"L",1000,"L",200]
#####################

while len(inst) > 0:
    pos,dir = doinst(inst,mapdata,pos,dir)
    cnt += 1
    if cnt % 1000 == 0:
        printmap(mapdata,path)
val = (1000 * (pos[1]+1)) + (4 * (pos[0]+1)) + dirval[dir]
print(val)

# 164034 is too high 
# 34468 is too low
# 15263 is too low
# 17319 is wrong
# 115311 is RIGHT!!!