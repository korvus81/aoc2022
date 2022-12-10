#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time
from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)


pp(lines)

data = [[int(r) for r in line] for line in lines]

#pp(data)

visible = make2dList(0, len(data[0]), len(data))

#pp(visible)

for row in range(len(data)):
    highest = -1
    for col in range(len(data[0])):
        if data[row][col] > highest:
            visible[row][col] = 1
        highest = max(highest,data[row][col])
    highest = -1
    for col in range(len(data[0])-1,-1,-1):
        if data[row][col] > highest:
            visible[row][col] = 1
        highest = max(highest,data[row][col])

for col in range(len(data[0])):
    highest = -1
    for row in range(len(data)):
        if data[row][col] > highest:
            visible[row][col] = 1
        highest = max(highest,data[row][col])
    highest = -1
    for row in range(len(data)-1,-1,-1):
        if data[row][col] > highest:
            visible[row][col] = 1
        highest = max(highest,data[row][col])


pp(["".join([str(c) for c in d]) for d in visible])
total = sum([sum(row) for row in visible])
print(total)