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

lines = ex 

pp(lines)

coords = [[int(x) for x in c.split(",")] for c in lines]
pp(coords)

# 6 sides on a cube
# 1,1,1 and 2,1,1 are connected because they are off by 1....
# when two cubes are connected, they each lose one side

sides_if_none_connected = len(coords) * 6

sides_lost_to_touching = 0
for ci1, c1 in enumerate(coords):
    for ci2 in range(ci1+1,len(coords)):
        c2 = coords[ci2]
        x1,y1,z1 = c1
        x2,y2,z2 = c2
        if x1==x2 and y1==y2 and abs(z1-z2) == 1:
            sides_lost_to_touching += 2
        if x1==x2 and z1==z2 and abs(y1-y2) == 1:
            sides_lost_to_touching += 2
        if z1==z2 and y1==y2 and abs(x1-x2) == 1:
            sides_lost_to_touching += 2
print(f"sides starting: {sides_if_none_connected}, sides lost: {sides_lost_to_touching}, surface area: {sides_if_none_connected-sides_lost_to_touching}")

