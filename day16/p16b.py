#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import re
import os
os.environ["COLUMNS"] = "220" # I usually keep my terminal around 240
from sys import exit
from collections import defaultdict,namedtuple
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

import time
from copy import deepcopy
import math 
import astar

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()

#lines = ex 
TIME_LIMIT = 26
START = "AA"

pp(lines)

pat = re.compile("Valve ([A-Za-z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Za-z, ]+)")
#lines = [pat.match(l).groups() for l in lines]
valves = {}
for l in lines:
    g = pat.match(l).groups()
    print(g)
    valves[g[0]] = {"name":g[0],"flow":int(g[1]),"others":[s.strip() for s in g[2].split(", ")]}
pp(valves)

cur = START 

def asneighbors(v):
    return valves[v]["others"]

distance_between_valves = {}
for v1 in valves.keys():
    if v1 not in distance_between_valves:
        distance_between_valves[v1] = {}
    for v2 in valves.keys():
        if v1 == v2:
            distance_between_valves[v1][v2]=0
            if v2 not in distance_between_valves:
                distance_between_valves[v2]= {}
            distance_between_valves[v2][v1]=0
        else:
            if v1 in distance_between_valves.get(v2,{}):
                distance_between_valves[v1][v2] = distance_between_valves[v2][v1]
            else:
                path = list(astar.find_path(v1,v2,asneighbors))
                distance_between_valves[v1][v2] = len(path)
                #print(f"path from {v1} to {v2} (len {len(path)})")
                #pp(path)
pp(distance_between_valves)

possible_valves = {vk for vk in valves.keys() if valves[vk]["flow"]>0}

def best_case_remaining_pressure(valves_open,mins_left):
    remaining_valves = possible_valves.difference(valves_open)
    remaining_flows = sorted([valves[r]["flow"] for r in remaining_valves],reverse=True)
    # can only open one valve every two minutes, since after opening one 
    # you'll have to move at least one minute to open another
    # multiplied by 2 since there are 2 of us moving
    m = (mins_left-1)*2
    tot = 0
    for r in remaining_flows:
        tot += r*m # flow times minutes left
        m -= 2
        if m <= 0: # ran out of minutes first
            return tot
    # ran out of remaining valves first
    return tot

def best_case_remaining_pressure2(st1,st2,valves_open,mins_left):
    remaining_valves = possible_valves.difference(valves_open)
    remaining_flows = sorted([valves[r]["flow"] for r in remaining_valves],reverse=True)
    # can only open one valve every two minutes, since after opening one 
    # you'll have to move at least one minute to open another
    # multiplied by 2 since there are 2 of us moving
    min_dist = min(min([distance_between_valves[st1][v] for v in remaining_valves]),min([distance_between_valves[st2][v] for v in remaining_valves]))
    m = (mins_left-min_dist)*2
    tot = 0
    for r in remaining_flows:
        tot += r*m # flow times minutes left
        m -= 2
        if m <= 0: # ran out of minutes first
            return tot
    # ran out of remaining valves first
    return tot


def priority(entry):
    curME = entry[0]
    curEL = entry[1]
    pathME = entry[2]
    #pathEL = entry[3]
    opened_valves = entry[4]
    pressure_released = entry[5]
    mins_left = TIME_LIMIT-len(pathME)
    rem = best_case_remaining_pressure2(curME,curEL,opened_valves, mins_left)
    
    # until we get close to the end, penalize theoretical benefits
    factor = 1.0
    if mins_left > 4:
        factor = 0.8
    elif mins_left > 10:
        factor = 0.2
    return -(pressure_released+round(factor*rem))



@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

paths = PriorityQueue()
# data format: (pri, ("AA"(me), "AA"(el), [AA, open, BB, open...](me), [AA, open, BB, open...](el), opened_valves=set(AA,BB), pressure_released))
start = (START,START,[],[],set(),0)
paths.put(PrioritizedItem(priority(start),start))
i = 0
while True:
    p = paths.get()
    if i % 10000 == 0:
        pp(p)
    curME,curEL,pathME,pathEL,opened_valves,pressure_released = p.item
    mins_left = TIME_LIMIT-len(pathME) # both should be the same length
    if mins_left == 0:
        pp(p.item)
        break
    memoves = []
    elmoves = []
    if valves[curME]["flow"] > 0 and curME not in opened_valves:
        ov = opened_valves.copy()
        ov.add(curME)
        it = (curME, pathME + ["OPEN "+curME], ov, (valves[curME]["flow"]*(mins_left-1)))
        memoves.append(it)
        #paths.put(PrioritizedItem(priority(it),it))
    if valves[curEL]["flow"] > 0 and curEL not in opened_valves:
        ov = opened_valves.copy()
        ov.add(curEL)
        it = (curEL, pathEL + ["OPEN "+curEL], ov, (valves[curEL]["flow"]*(mins_left-1)))
        elmoves.append(it)
        #paths.put(PrioritizedItem(priority(it),it))
    for o in valves[curME]["others"]:
        if len(pathME) < 1 or o != pathME[-1]: # avoid going directly back where you were if you didn't even open a valve
            it = (o, pathME + [o], opened_valves, 0) # last is EXTRA pressure released
            memoves.append(it)
            #paths.put(PrioritizedItem(priority(it),it))
    for o in valves[curEL]["others"]:
        if len(pathEL) < 1 or o != pathEL[-1]: # avoid going directly back where you were if you didn't even open a valve
            it = (o, pathEL + [o], opened_valves, 0) # last is EXTRA pressure released
            elmoves.append(it)
            #paths.put(PrioritizedItem(priority(it),it))
    for elm in elmoves:
        for mem in memoves:
            el_last = elm[1][-1]
            me_last = mem[1][-1]
            if el_last.startswith("OPEN") and el_last == me_last:
                pass # skip the case where we both open the same valve
            else:
                it = (mem[0], elm[0], mem[1], elm[1], mem[2].union(elm[2]), pressure_released+mem[3]+elm[3])
                paths.put(PrioritizedItem(priority(it), it))

    i += 1

print("====")
pp(paths.get())
pp(paths.get())
pp(paths.get())
pp(paths.get())