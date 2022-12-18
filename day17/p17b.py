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
jets = list(lns)[0]

ex = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""
#jets = ex


rocks = [
    ["####"],
    [".#.","###",".#."],
    ["..#","..#","###"],
    ["#","#","#","#"],
    ["##","##"]
]


pp(jets)
empty_row = [" "]*7
tunnel = [["-"]*7,[" "]*7,[" "]*7,[" "]*7]

jet_ind = 0
rock_ind = 0

def display_tunnel(tunnel):
    for row in tunnel[::-1]:
        print("|"+("".join(row))+"|")
    print()

def display_tunnel_with_rock(tunnel,rock,rock_pos):
    y = len(tunnel)-1
    rock_height = len(rock)
    for row in tunnel[::-1]:
        print("|",end="")
        if y > rock_pos[1] or y < (rock_pos[1]-rock_height+1):
            print("".join(row),end="")
        else:
            rock_y = rock_pos[1]-y
            rock_row = rock[rock_y]
            for tunx,ch in enumerate(row):
                if tunx < rock_pos[0] or tunx >= rock_pos[0]+len(rock_row):
                    print(ch,end="")
                else:
                    if rock_row[tunx-rock_pos[0]] == "#":
                        print("@",end="")
                    else:
                        print(ch,end="")

        print("|")
        y = y - 1
    print()



def can_move(tunnel,rock,pos):
    if pos[0] < 0 or pos[0] >= 7:
        return False
    if pos[1] < 1:
        return False
    for y,rockrow in enumerate(rock):
        for x,ch in enumerate(rockrow):
            tmpx = pos[0]+x
            tmpy = pos[1]-y
            if tmpx >= 7:
                return False
            #print(f"tmpx={tmpx} tmpy={tmpy}")
            if ch == "#" and tunnel[tmpy][tmpx] != " ":
                return False
    return True 

def fingerprint(tunnel):
    ind = len(tunnel) - 1
    while all([ch == " " for ch in tunnel[ind]]):
        ind=ind-1
    # should be on a non-empty row now
    fingerprint = 0
    for yd in range(30): # should be enough?
        row = tunnel[ind-yd]
        rowval = 0
        for ch in row:
            rowval = rowval * 2
            if ch == "#":
                rowval += 1
        fingerprint = fingerprint * 256
        fingerprint += rowval
    return fingerprint

fingerprints_to_rows = dict()


last_height = 0
for i in range(1000000000000):
    rock = rocks[rock_ind]
    rock_height = len(rock)
    empty_row_count = 0
    ind = len(tunnel)-1
    while tunnel[ind] == empty_row:
        empty_row_count+=1
        ind -=1
    empty_rows_needed = 3 + rock_height
    for j in range(empty_rows_needed-empty_row_count):
        tunnel.append([x for x in empty_row])
    empty_row_count = 0
    for row in tunnel[::-1]:
        if all([ch == " " for ch in row]):
            empty_row_count += 1
        else:
            break
    
    if i % 10000 == 0 or i == 1440:
        height = len(tunnel)-1
        while all([ch == " " for ch in tunnel[height]]):
            height = height-1
        
        print(f"[{i}] {100.0*float(i)/1000000000000.0}% done  height = {height} ({height-last_height} increase)")
        last_height = height
        display_tunnel(tunnel[-100:])
    #if i % 200 == 0:
    #    display_tunnel(tunnel)
    
    
    rock_pos = (2,len(tunnel)-1)

    if empty_row_count > empty_rows_needed:
        rock_pos = (2,len(tunnel)-1-(empty_row_count-empty_rows_needed))

    falling = True
    while falling:
        jet = jets[jet_ind]
        if jet == ">":
            new_rock_pos = (rock_pos[0]+1,rock_pos[1])
        elif jet == "<":
            new_rock_pos = (rock_pos[0]-1,rock_pos[1])
        if can_move(tunnel,rock,new_rock_pos):
            rock_pos = new_rock_pos
        #print(f"After jet {jet}:")
        #display_tunnel_with_rock(tunnel,rock,rock_pos)
        jet_ind = (jet_ind + 1) % len(jets)

        if can_move(tunnel,rock,(rock_pos[0],rock_pos[1]-1)):
            rock_pos = (rock_pos[0],rock_pos[1]-1)
        else: # time to place rock!
            for yd,rock_row in enumerate(rock):
                for xd,ch in enumerate(rock_row):
                    if ch == "#":
                        tunnel[rock_pos[1]-yd][rock_pos[0]+xd] = "#"
            rock_ind = (rock_ind + 1) % len(rocks)
            falling = False 
        #print("After fall:")
        #display_tunnel_with_rock(tunnel,rock,rock_pos)
    if i > 20:
        fp = fingerprint(tunnel)
        height = len(tunnel)-1
        while all([ch == " " for ch in tunnel[height]]):
            height = height-1

        if fp in fingerprints_to_rows:
            
            print(f"after rock {i}, fingerprint {fp} found = {fingerprints_to_rows[fp]}")
            fingerprints_to_rows[fp].append((i,height))
        else:
            fingerprints_to_rows[fp] = [(i,height)]
    #print("===========")

#display_tunnel(tunnel)
height = len(tunnel)-1
while all([ch == " " for ch in tunnel[height]]):
    height = height-1
print(f"height = {height}")


# >>> a = [(1434, 2277), (3154, 5015), (4874, 7753), (6594, 10491), (8314, 13229)]
# >>> heights=list(zip(*a))[1]
# >>> rocknums=list(zip(*a))[0]
# >>> [rocknums[i]-rocknums[i-1] for i in range(1,len(rocknums))]
# [1720, 1720, 1720, 1720]
# >>> [heights[i]-heights[i-1] for i in range(1,len(heights))]
# [2738, 2738, 2738, 2738]
# >>> 1000000000000/1720
# 581395348.8372093
# >>> 1000000000000-(1720*581395348)
# 1440