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

ex = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()
#lines = ex 


data1 = {x[0]:x[1] for x in [l.split(": ") for l in lines]}
data = {}
for k,v in data1.items():
    if "+" in v:
        parts = v.split(" + ")
        v1 = ("+", parts[0].strip(), parts[1].strip())
    elif "-" in v:
        parts = v.split(" - ")
        v1 = ("-", parts[0].strip(), parts[1].strip())
    elif "*" in v:
        parts = v.split(" * ")
        v1 = ("*", parts[0].strip(), parts[1].strip())
    elif "/" in v:
        parts = v.split(" / ")
        v1 = ("/", parts[0].strip(), parts[1].strip())
    else:
        v1 = ("int", int(v))
    data[k] = v1

pp(data)

def build_tree(d,rootkey="root"):
    root = d[rootkey]
    if root[0] == "int":
        ret = root[1]
    elif root[0] == "+":
        ret = build_tree(d,root[1]) + build_tree(d,root[2])
    elif root[0] == "-":
        ret = build_tree(d,root[1]) - build_tree(d,root[2])
    elif root[0] == "/":
        ret = build_tree(d,root[1]) / build_tree(d,root[2])
    elif root[0] == "*":
        ret = build_tree(d,root[1]) * build_tree(d,root[2])
    else:
        print(f"ERROR {root}")
    print(f"[{rootkey}] {root} -> {ret}")
    return ret
    

tree = build_tree(data)
pp(tree)
# 223971851179174.0