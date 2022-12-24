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
from datetime import datetime
from copy import deepcopy
import math 
import astar

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines()
#lines = ex

mapdata = lines
pp(mapdata)

blank_map = [ln.replace("^",".").replace("v",".").replace("<",".").replace(">",".") for ln in lines]
pp(blank_map)

exped_start = (0,0)
for x,ch in enumerate(mapdata[0]):
    if ch == ".":
        exped_start = (x,0)
print(f"start={exped_start}")

blizzards = []
for y,ln in enumerate(mapdata):
    for x,ch in enumerate(ln):
        match ch:
            case "^":
                blizzards.append((x,y,"U"))
            case "v":
                blizzards.append((x,y,"D"))
            case "<":
                blizzards.append((x,y,"L"))
            case ">":
                blizzards.append((x,y,"R"))
            case ".":
                if y == len(mapdata)-1:
                    exped_end = (x,y)
pp(blizzards)
print(f"end={exped_end}")
map_height = len(mapdata)
map_width = len(mapdata[0])

def next_blizzard_pos(blizzards,map_height,map_width):
    new_blizzards = []
    for x,y,dir in blizzards:
        match dir:
            case "U":
                if y == 1:
                    new_blizzards.append((x,map_height-2,dir)) # -2 because -1 would be the wall
                else:
                    new_blizzards.append((x,y-1,dir)) 
            case "D":
                if y == map_height-2:
                    new_blizzards.append((x,1,dir)) # 1 because 0 would be the wall
                else:
                    new_blizzards.append((x,y+1,dir)) 
            case "L":
                if x == 1:
                    new_blizzards.append((map_width-2,y,dir)) # -2 because -1 would be the wall
                else:
                    new_blizzards.append((x-1,y,dir)) 
            case "R":
                if x == map_width-2:
                    new_blizzards.append((1,y,dir)) # 1 because -0 would be the wall
                else:
                    new_blizzards.append((x+1,y,dir)) 
    return new_blizzards



def possible_moves(start,goal,next_blizzards, next_blizzards_set, map_height, map_width):
    #next_blizzards = next_blizzard_pos(blizzards,map_height,map_width)
    #next_blizzards_set = set([(b[0],b[1]) for b in next_blizzards])
    positions_to_try = [start] # this covers staying still
    valid_positions = []
    x,y = start 
    if y > 0:
        positions_to_try.append((x,y-1))
    if y < map_height-1:
        positions_to_try.append((x,y+1))
    if x > 1: # all x==0 is a wall
        positions_to_try.append((x-1,y))
    if x < map_width-2: # all x==map_width-1 is a wall
        positions_to_try.append((x+1,y))
    for newx,newy in positions_to_try:
        if mapdata[newy][newx] == "#":
            continue # skip this if it is a wall
        if (newx,newy) in next_blizzards_set:
            continue
        valid_positions.append((newx,newy))
    return valid_positions

def print_map(pos,blizzards):
    blizzards_set = set([(b[0],b[1]) for b in blizzards])
    if pos is not None:
        myx,myy = pos
    else:
        myx = -1
        myy = -1
    for y,ln in enumerate(blank_map):
        for x,ch in enumerate(ln):
            if myx == x and myy == y:
                p("[red]E[/red]",end="")
            elif (x,y) in blizzards_set:
                ch = "?"
                for b in blizzards:
                    if b[0]==x and b[1]==y:
                        if ch == "?":
                            ch = b[2].replace("R",">").replace("L","<").replace("U","^").replace("D","v")
                        else:
                            if ch in "<>^vRLUD":
                                ch = "2"
                            else:
                                ch = str(int(ch)+1)[0]
                p(f"[blue]{ch}[/blue]",end="")
            else:
                p(f"[green]{ch}[green]",end="")
        print()
    print()


pos = exped_start
print_map(pos,blizzards)

@lru_cache
def blizzards_for_step(stepnum,map_height,map_width):
    if stepnum == 0:
        blizzards_set = set([(b[0],b[1]) for b in blizzards])
        return blizzards,blizzards_set
    else:
        last_blizzards,last_blizzards_set = blizzards_for_step(stepnum-1,map_height,map_width)
        bpos = next_blizzard_pos(last_blizzards,map_height,map_width)
        blizzards_set = set([(b[0],b[1]) for b in bpos])
        return bpos,blizzards_set

def heuristic(move):
    pos,step_num,path = move
    dist = abs(exped_end[0]-pos[0]) + abs(exped_end[1]-pos[1])
    return -dist # I was using step num, but I think these will all be at the same distance when I run it

done = False
latest_step = 0
moves = [(pos,0,[])]

st = datetime.now()
while not done:
    move_pos,step_num,path = moves.pop() # pop from end
    if step_num > latest_step:
        latest_step = step_num
        moveset = set()
        new_moves = []
        for m in moves:
            move_pos2,step_num2,path2 = m
            if (move_pos2,step_num2) not in moveset:
                new_moves.append(m)
                moveset.add((move_pos2,step_num2))
        print(f"[{step_num}] had {len(moves)} moves but reduced to {len(new_moves)} by removing duplicates...")
        moves = new_moves
        moves.sort(key=heuristic)
        if len(moves) > 100000:
            print(f"[{step_num}] Pruning {len(moves)} moves to 100000...")
        moves = moves[-100000:] # keep no more than 10000 best
        if step_num % 20 == 0:
            best_move = moves[0]
            print(f"Best move @ {best_move[1]} steps, time = {datetime.now()-st}")
            bliz,bliz_set = blizzards_for_step(best_move[1], map_height, map_width)
            print_map(best_move[0],bliz)
    next_bliz,next_bliz_set = blizzards_for_step(step_num+1, map_height, map_width)
    pos_moves = possible_moves(move_pos,exped_end, next_bliz, next_bliz_set, map_height, map_width)
    for pm in pos_moves:
        moves.insert(0,(pm,step_num+1,path + [pm])) # insert at front
        if pm[0] == exped_end[0] and pm[1] == exped_end[1]:
            print(f"Solution found: {pm}\nSteps: {step_num+1}\nPath: {path}")
            time.sleep(2)
            done = True 