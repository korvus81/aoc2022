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
TIME_LIMIT = 30
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

#@lru_cache(maxsize=100000)
def flow(valves_opened):
    f = sum(valves[v]["flow"] for v in valves_opened)
    #print(f"valves={valves_opened} flow={f}")
    return f


#@lru_cache(maxsize=100000)
def findBestPath(cur_path, mins_left, valves_opened=None, pressure_released=0, blacklisted_valves=None):
    if valves_opened is None:
        valves_opened = set()
    if blacklisted_valves is None:
        blacklisted_valves = set()
    if mins_left == 0 or len(valves_opened) == nonzero_valves:
        #print(f"cur_path={cur_path}, mins_left={mins_left}, valves_opened={valves_opened}")
        return cur_path,valves_opened,pressure_released
    cur_valve = cur_path[-1]
    possible_paths = []
    if cur_valve not in valves_opened and valves[cur_valve]["flow"] > 0:
        #print(f"opening {cur_valve}")
        vo = set(valves_opened)
        vo.add(cur_valve)
        if len(valves[cur_valve]["others"]) <= 1:
            bv = blacklisted_valves.copy()
            bv.add(cur_valve)
            blacklisted_valves = bv
        possible_paths.append(findBestPath(cur_path, mins_left-1, vo, pressure_released+(valves[cur_valve]["flow"]*(mins_left-1)), blacklisted_valves))
    if mins_left >= 1:
        for v in valves[cur_valve]["others"]:
            if v not in blacklisted_valves:
                possible_paths.append(findBestPath(cur_path+[v], mins_left-1, valves_opened.copy(), pressure_released, blacklisted_valves))
    possp = sorted(possible_paths,key=lambda p:p[1])
    #pp(possp)
    #print()
    if len(possp) == 0:
        return cur_path,valves_opened,pressure_released
    return possp[-1]

#p = findBestPath([cur], 20, valves_opened=frozenset())


possible_valves = {vk for vk in valves.keys() if valves[vk]["flow"]>0}

def best_case_remaining_pressure(valves_open,mins_left):
    remaining_valves = possible_valves.difference(valves_open)
    remaining_flows = sorted([valves[r]["flow"] for r in remaining_valves],reverse=True)
    # can only open one valve every two minutes, since after opening one 
    # you'll have to move at least one minute to open another
    m = mins_left-1
    tot = 0
    for r in remaining_flows:
        tot += r*m # flow times minutes left
        m -= 2
        if m <= 0: # ran out of minutes first
            return tot
    # ran out of remaining valves first
    return tot

def priority(entry):
    #cur = entry[0]
    path = entry[1]
    opened_valves = entry[2]
    pressure_released = entry[3]
    rem = best_case_remaining_pressure(opened_valves, TIME_LIMIT-len(path))
    return -(pressure_released+rem)    



@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

paths = PriorityQueue()
# data format: (pri, ("AA", [AA, open, BB, open...], opened_valves=set(AA,BB), pressure_released))
start = (START,[],set(),0)
paths.put(PrioritizedItem(priority(start),start))
i = 0
while True:
    p = paths.get()
    if i % 1000 == 0:
        pp(p)
    cur,path,opened_valves,pressure_released = p.item
    mins_left = TIME_LIMIT-len(path)
    if mins_left == 0:
        pp(p.item)
        break
    if valves[cur]["flow"] > 0 and cur not in opened_valves:
        ov = opened_valves.copy()
        ov.add(cur)
        it = (cur, path + ["OPEN "+cur], ov, pressure_released+(valves[cur]["flow"]*(mins_left-1)))
        paths.put(PrioritizedItem(priority(it),it))
    for o in valves[cur]["others"]:
        it = (o, path + [o], opened_valves, pressure_released)
        paths.put(PrioritizedItem(priority(it),it))
    i += 1

print("====")
pp(paths.get())
pp(paths.get())
pp(paths.get())
pp(paths.get())