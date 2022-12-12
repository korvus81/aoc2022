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

ex = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()

#lines = ex 
pp(lines)
splitlines = [ln.split() for ln in lines]
#data = [ (l[0],int(l[1])) for l in splitlines if l[0] == "addx" else ("noop",0)]
#pp(data)
data = []
altdata = []
for l in lines:
    if l.startswith("noop"):
        data.append(("noop",0))
        altdata.append(("noop",0))
    elif l.startswith("addx"):
        ls = l.split()
        data.append((ls[0],int(ls[1])))
        altdata.append(("noop",-1))
        altdata.append((ls[0],int(ls[1])))
    else:
        print(f"ERROR = {l}")
pp(altdata)

def drawscreen(screen):
    print("".join(screen[0:40]))
    print("".join(screen[40:80]))
    print("".join(screen[80:120]))
    print("".join(screen[120:160]))
    print("".join(screen[160:200]))
    print("".join(screen[200:240]))

cycle = 0
xreg = 1
sigstr = []
screen = [' ' for i in range(240)]
for d in altdata:
    cycle += 1
    curpx = (cycle-1) % len(screen)
    hpos = (curpx % 40) 
    if hpos in [xreg, xreg-1, xreg+1]:
        screen[curpx] = "#"
    else:
        screen[curpx] = "."
    if cycle >= 20 and (cycle-20) % 40 == 0:
        sstr = cycle * xreg
        print(f"[cycle {cycle}] sstr={sstr} sigstr={sigstr}")
        sigstr.append(sstr)
    print(f"[{cycle}] {d} xreg={xreg} hpos={hpos} curpx+1={curpx+1} drawn={screen[curpx]}")
    if d[0] == "noop":
        pass
    elif d[0] == "addx":
        xreg += d[1]
        
pp(sigstr)
print(f"sum = {sum(sigstr)}")
drawscreen(screen)