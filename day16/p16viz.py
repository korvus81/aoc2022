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
import graphviz
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
dot = graphviz.Graph('p16', comment='AoC2022 Day 16',format="png",engine="twopi")  
for k,v in valves.items():
    if k == "AA":
        dot.node(k, f"{k}",root="true")
    elif v['flow'] == 0:
        dot.node(k, f"{k}")
    else:
        dot.node(k, f"{k} - {v['flow']}")
edges = set()
for k,v in valves.items():
    for o in v["others"]:
        if k < o:
            edges.add((k,o))
        else:
            edges.add((o,k))
for edge in edges:
    dot.edge(*edge)

dot.render("p16.dot",view=True)
