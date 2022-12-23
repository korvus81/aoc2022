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

smallex = """.....
..##.
..#..
.....
..##.
.....""".splitlines()

ex = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""".splitlines()
lines = ex 


def alone(pos,elves_set):
    possible_locs = set()
    x = pos[0]
    y = pos[1]
    for x2 in range(x-1,x+1+1):
        for y2 in range(y-1,y+1+1):
            if x == x2 and y == y2:
                pass
            else:
                possible_locs.add((x2,y2))
    #print(f"Checking {pos} for elves in {possible_locs}")
    return possible_locs.isdisjoint(elves_set)

def can_go(pos, dir, elves_set):
    x = pos[0]
    y = pos[1]
    match dir:
        case "N":
            return ((x-1,y-1) not in elves_set and (x,y-1) not in elves_set and (x+1,y-1) not in elves_set), (x,y-1)
        case "S":
            return ((x-1,y+1) not in elves_set and (x,y+1) not in elves_set and (x+1,y+1) not in elves_set), (x,y+1)
        case "E":
            return ((x+1,y-1) not in elves_set and (x+1,y) not in elves_set and (x+1,y+1) not in elves_set), (x+1,y)
        case "W": 
            return ((x-1,y-1) not in elves_set and (x-1,y) not in elves_set and (x-1,y+1) not in elves_set), (x-1,y)



elves = []
for y,row in enumerate(lines):
    for x,ch in enumerate(row):
        if ch == "#":
            elves.append((x,y))



pp(lines)
pp(elves)

def getBounds(elves):
    minx = elves[0][0]
    maxx = elves[0][0]
    miny = elves[0][1]
    maxy = elves[0][1]
    for elf in elves:
        x,y = elf
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x 
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    return minx,maxx,miny,maxy

def drawField(elves,elves_set):
    empty = 0
    minx,maxx,miny,maxy = getBounds(elves)
    p(" ",end="")
    for x in range(minx,maxx+1):
        p(f"{str(x)[-1]}",end="")
    print()
    for y in range(miny,maxy+1):
        p(f"{str(y)[-1]}",end="")
        for x in range(minx,maxx+1):
            if (x,y) in elves_set:
                p("[green]#[/green]",end="")
            else:
                p("[gray].[/gray]",end="")
                empty += 1
        print()
    print()
    return empty 

dirOrder = ["N","S","W","E"]


move_round = 1
changed = True
while changed:
    changed = False 
    print(f"ROUND {move_round}")
    elves_set = set(elves)
    proposals = {} # map of proposed location to list of elves
    #drawField(elves,elves_set)

    for elf in elves:
        proposed = False
        if not alone(elf,elves_set):
            for dir in dirOrder:
                cg,prop_loc = can_go(elf,dir,elves_set)
                if cg:
                    if prop_loc not in proposals:
                        proposals[prop_loc] = []
                    proposals[prop_loc].append(elf)
                    proposed = True
                    break # break out of dir iteration
            if not proposed:
                pass
                #print(f"Elf {elf} had no proposals!")
        else:
            pass
            #print(f"Elf {elf} has no neighbors, so staying put")

    for prop,elf_list in proposals.items():
        if len(elf_list) == 1:
            #print(f"moving elf {elf_list[0]} to {prop}")
            elves.remove(elf_list[0])
            elves.append(prop)
            changed = True
        else:
            pass
            #print(f"elves {elf_list} all wanted to move to {prop}, so staying put!")
    #pp(elves)
    dirOrder = dirOrder[1:] + [dirOrder[0]]     
    #pp(dirOrder)
    move_round += 1 
    

empty = drawField(elves,elves_set)
print(f"move_round={move_round-1}")
print(empty)
# not 926
# duh, 925