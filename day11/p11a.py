#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time
import math
from util import *
from aocd import lines as lns  # like data.splitlines()
from copy import deepcopy
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()

#lines = ex 


pp(lines)

monkeys = []
for ln in lines:
    if ln.startswith("Monkey "):
        monkeys.append({"inspections":0}) # just assume they are counted 0->(num_monkeys-1)
    elif ln.startswith("  Starting items: "):
        items = line_to_num_list(ln)
        pp(items)
        monkeys[-1]["items"] = items 
    elif ln.startswith("  Operation: "):
        optxt = ln[len("  Operation: "):].replace("new = ","lambda old: ").strip()
        print(optxt)
        fop = eval(optxt)
        print(f"example old=4 -> {fop(4)}, old=5 -> {fop(5)}")
        monkeys[-1]["op"] = fop
    elif ln.startswith("  Test: divisible by "):
        divby = int(ln[len("  Test: divisible by "):].strip())
        monkeys[-1]["divbytest"] = divby
        monkeys[-1]["testfunc"] = lambda x: (x % divby) == 0 ## broken???
    elif ln.startswith("    If "):
        if ln.startswith("    If true: throw to monkey "):
            monkeys[-1]["truedest"] = int(ln[len("    If true: throw to monkey "):].strip())
        elif ln.startswith("    If false: throw to monkey "):
            monkeys[-1]["falsedest"] = int(ln[len("    If false: throw to monkey "):].strip())


pp(monkeys)

def round_of_monkeys(monkeys_in):
    monkeys = deepcopy(monkeys_in)
    for mix,m in enumerate(monkeys):
        items = m["items"]
        for item in items:
            monkeys[mix]["inspections"] += 1
            itval = m["op"](item)
            itval2 = int(math.floor(itval / 3))
            print(f"monkey {mix}: {item} -> {itval} -> {itval2}")
            if (itval2 % m["divbytest"]) == 0:
                monkeys[m["truedest"]]["items"].append(itval2)
                print(f"  item of worry value {itval2} thrown to monkey {m['truedest']} [TRUE]")
            else:
                monkeys[m["falsedest"]]["items"].append(itval2)
                print(f"  item of worry value {itval2} thrown to monkey {m['falsedest']} [FALSE]")
        monkeys[mix]["items"] = [] # all thrown
    return monkeys 

for i in range(20):
    print(f"==== ROUND {i+1} ====")
    monkeys = round_of_monkeys(monkeys)
    pp(monkeys)
    for mix,m in enumerate(monkeys):
        print(f"[{mix}({m['inspections']})]: {m['items']}")

smonkeys = sorted(monkeys,key=lambda m:m["inspections"])
print(f"top two: {smonkeys[-1]['inspections']} x {smonkeys[-2]['inspections']} = {smonkeys[-1]['inspections'] * smonkeys[-2]['inspections']}")