#from pprint import pprint as pp 
import itertools
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
import networkx as nx


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



G = nx.Graph()
for v in valves.keys():
    G.add_node(v)
    for ot in valves[v]["others"]:
        G.add_edge(v,ot)
#pos = nx.planar_layout(G)
#nx.draw(G, pos, with_labels = True)
#nx.draw_networkx_edge_labels(G, pos,edge_labels=edge_labels)

fw = nx.floyd_warshall(G, weight='weight')

node_distances = {a:dict(b) for a,b in fw.items()}  
pp(node_distances)
pp(node_distances["AA"])

possible_valves = {vk for vk in valves.keys() if valves[vk]["flow"]>0}

def findSolutions(possible_valves):
    print(f"len(possible_valves)={len(possible_valves)}")
    solutions = []
    count = 0
    for valve_order in itertools.permutations(possible_valves,8):
        mins_left = TIME_LIMIT
        cur_pos = START
        path = []
        pressure_released = 0
        for v in valve_order:
            distance = node_distances[cur_pos][v]
            if distance >= mins_left:
                break # done, go save this
            mins_left -= distance
            mins_left -= 1 # time to open the valve
            cur_pos = v
            path.append(v)
            pressure_released += int(valves[v]["flow"] * mins_left)
            
        solutions.append((pressure_released, tuple(path)))
        count += 1
        if count % 1000000 == 0:
            print(f"count={count}/259_459_200 P(15,8), len(solutions)={len(solutions)}") # 259_459_200 P(15,8) # 32_432_400 P(15,7)
            solutions.sort()
            solutions = list(set(solutions))
            #solutions = list(set(solutions[-100000:]))
            solutions.sort()
            pp(solutions[-1])
    solutions = list(set(solutions))
    solutions.sort()
    return solutions

solutions = findSolutions(possible_valves)
print(f"len(solutions)={len(solutions)}") 
lens = [len(s[1]) for s in solutions]
distinct_lens = set(lens)
len_counts = {length:lens.count(length) for length in sorted(distinct_lens) }
pp(len_counts)
pp(solutions[-50:])

print("=========")

best_pressure_so_far = 0
best_solutions = []
count = 0
for sol in solutions[::-1]:
    print(f"==== Looking for matches for solution {sol} @ {sol[0]} pressure released...")
    sol_pressure = sol[0]
    poss_valves = possible_valves.difference(set(sol[1])) #remove visited valves
    elsols = findSolutions(poss_valves)
    print(f"Found {len(elsols)} solutions! Best is {sol_pressure} + {elsols[-1][0]} = {sol_pressure+elsols[-1][0]} pressure!")
    pp(elsols[-5:])
    best_pres = sol_pressure+elsols[-1][0]
    if best_pres > best_pressure_so_far:
        best_pressure_so_far = best_pres 
        best_solutions = [sol,elsols[-1]]
    print()
    count = count + 1
    if count % 10 == 0:
        print(f">>>> best pressure so far: {best_pressure_so_far} from: {best_solutions}")
    print()
    


time.sleep(100)

simplified_valves = {}
for v in valves.keys():
    simplified_valves[v] = valves[v]
    simplified_valves[v]["weighted_others"] = {ot:1 for ot in valves[v]["others"]}

changed = True 
while changed:
    changed = False
    nodes_to_delete = []
    for v in simplified_valves.keys():    
        valve = simplified_valves[v]
        woth = valve["weighted_others"]
        if v != "AA" and valve["flow"] == 0 and len(woth) == 2:
            woth_keys = list(woth.keys())
            ov1 = woth_keys[0]
            ov2 = woth_keys[1]
            ov1w = woth[ov1]
            ov2w = woth[ov2]
            # ov1w,ov1 = woth_keys[0]
            # ov2w,ov2 = woth_keys[1]
            simplified_valves[ov1]["weighted_others"][ov2] = ov1w + ov2w 
            simplified_valves[ov2]["weighted_others"][ov1] = ov1w + ov2w 
            del simplified_valves[ov1]["weighted_others"][v]
            del simplified_valves[ov2]["weighted_others"][v]
            nodes_to_delete.append(v)
    for v in nodes_to_delete:
        del simplified_valves[v]
        changed = True
    pp(simplified_valves)
    print("===")

cur = START 

def asneighbors(v):
    return valves[v]["others"]

distance_between_valves = {}
for v1 in valves.keys():
    if valves[v1]["flow"] > 0 or v1 == "AA":
        if v1 not in distance_between_valves:
            distance_between_valves[v1] = {}
        for v2 in valves.keys():
            if valves[v2]["flow"] > 0 or v2 == "AA":
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
    m = (mins_left-min_dist)
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
    pathEL = entry[3]
    opened_valves = entry[4]
    pressure_released = entry[5]
    mins_left = TIME_LIMIT*2-len(pathME)-len(pathEL)
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

#start = (START,START,[],[],set(),0)
start_wo = simplified_valves[START]["weighted_others"]
start_keys = start_wo.keys()
for k1 in start_keys:
    for k2 in start_keys:
        if k1 != k2: # theoretically they could start going in the same direction, but lets try this...
            it = (k1,k2,[k1]*start_wo[k1], [k2]*start_wo[k2], set(), 0)
            paths.put(PrioritizedItem(priority(it),it))

#paths.put(PrioritizedItem(priority(start),start))
i = 0
while True:
    p = paths.get()
    if i % 10000 == 0:
        pp(p)
    if i % 100000 == 0 and i > 1000:
        newpaths = PriorityQueue()

    curME,curEL,pathME,pathEL,opened_valves,pressure_released = p.item
    mins_leftME = TIME_LIMIT-len(pathME)
    mins_leftEL = TIME_LIMIT-len(pathEL)
    remaining_valves = possible_valves.difference(opened_valves)
    if len(remaining_valves) == 0:
        pp(p)
        break
    memoves = []
    elmoves = []
    if mins_leftME > 0:
        if simplified_valves[curME]["flow"] > 0 and curME not in opened_valves:
            ov = opened_valves.copy()
            ov.add(curME)
            it = (curME, pathME + ["OPEN "+curME], ov, (simplified_valves[curME]["flow"]*(mins_leftME-1)))
            memoves.append(it)
            #paths.put(PrioritizedItem(priority(it),it))
        for o in simplified_valves[curME]["weighted_others"].keys():
            if len(pathME) < 1 or o != pathME[-1]: # avoid going directly back where you were if you didn't even open a valve
                it = (o, pathME + [o]*simplified_valves[curME]["weighted_others"][o], opened_valves, 0) # last is EXTRA pressure released
                memoves.append(it)
                #paths.put(PrioritizedItem(priority(it),it))
    if mins_leftEL > 0:
        if simplified_valves[curEL]["flow"] > 0 and curEL not in opened_valves:
            ov = opened_valves.copy()
            ov.add(curEL)
            it = (curEL, pathEL + ["OPEN "+curEL], ov, (simplified_valves[curEL]["flow"]*(mins_leftEL-1)))
            elmoves.append(it)
            #paths.put(PrioritizedItem(priority(it),it))
        
        for o in simplified_valves[curEL]["weighted_others"].keys():
            if len(pathEL) < 1 or o != pathEL[-1]: # avoid going directly back where you were if you didn't even open a valve
                it = (o, pathEL + [o]*simplified_valves[curEL]["weighted_others"][o], opened_valves, 0) # last is EXTRA pressure released
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