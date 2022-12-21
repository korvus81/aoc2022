from pprint import pprint as pp2
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
import numbers

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
data["root"] = ("=", data["root"][1],data["root"][2])

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
    

def build_tree2(d,rootkey="root",humn = "HUMN"):
    root = d[rootkey]
    a = None
    b = None
    if rootkey == "humn":
        ret = "HUMN"
    elif root[0] == "int":
        ret = root[1]
    elif root[0] == "+":
        a = build_tree2(d,root[1],humn)
        b = build_tree2(d,root[2],humn)
        if isinstance(a,numbers.Number) and isinstance(b,numbers.Number):
            ret = a + b
        else: 
            ret = ("+", a, b)
    elif root[0] == "-":
        a = build_tree2(d,root[1],humn)
        b = build_tree2(d,root[2],humn)
        if isinstance(a,numbers.Number) and isinstance(b,numbers.Number):
            ret = a - b
        else: 
            ret = ("-", a, b)
        
    elif root[0] == "/":
        a = build_tree2(d,root[1],humn)
        b = build_tree2(d,root[2],humn)
        if isinstance(a,numbers.Number) and isinstance(b,numbers.Number):
            ret = a / b
        else: 
            ret = ("/", a, b)
    elif root[0] == "*":
        a = build_tree2(d,root[1],humn)
        b = build_tree2(d,root[2],humn)
        if isinstance(a,numbers.Number) and isinstance(b,numbers.Number):
            ret = a * b
        else: 
            ret = ("*", a, b)
    elif root[0] == "=":
        a = build_tree2(d,root[1],humn)
        b = build_tree2(d,root[2],humn)
        # if isinstance(a,numbers.Number) and isinstance(b,numbers.Number):
        #     ret = a == b
        # else: 
        #     ret = ("=", a, b)
        ret = ("=", a, b)
    else:
        print(f"ERROR {root}")
    print(f"[{rootkey}] {root} (a={a}, b={b}) -> {ret}")
    return ret

def print_tree(tree,indent=0):
    ind = "  "*indent
    if isinstance(tree,numbers.Number):
        print(ind+str(tree))
        return
    elif isinstance(tree,str):
        print(ind+str(tree))
        return
    else:
        print(ind+str(tree[0]))
        print_tree(tree[1],indent+1)
        print_tree(tree[2],indent+1)
    

tree = build_tree2(data,"root","HUMN")
print(tree)
pp2(tree)
print_tree(tree[1])
print()
print("left:")
print(tree[1])
print("right:")
print(tree[2])
right = tree[2] # this is the numeric one

def simplify(root,ans):
    if root[0] == "+": 
        if isinstance(root[1],numbers.Number):
            return root[2],ans-root[1]
        elif isinstance(root[2],numbers.Number):
            return root[1],ans-root[2]
    elif root[0] == "-":
        if isinstance(root[1],numbers.Number):
            return root[2],root[1]-ans
        elif isinstance(root[2],numbers.Number):
            return root[1],ans+root[2]
    elif root[0] == "/":
        if isinstance(root[1],numbers.Number):
            return root[2],root[1]/ans
        elif isinstance(root[2],numbers.Number):
            return root[1],ans*root[2]
    elif root[0] == "*":
        if isinstance(root[1],numbers.Number):
            return root[2],ans/root[1]
        elif isinstance(root[2],numbers.Number):
            return root[1],ans/root[2]
    elif root[0] == "=":
        print(f"ERROR {root}")
    else:
        print(f"ERROR {root}")
    return None,0

new_tree = tree[1]
new_right = right
while True:
    new_tree, new_right = simplify(new_tree, new_right)

    print(new_right)
    print_tree(new_tree)
    print()


# 3379022190351