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

ex = """1
2
-3
3
-2
0
4""".splitlines()
#lines = ex

DECRYPTION_KEY = 811589153


lines = [int(l)*DECRYPTION_KEY for l in lines]
#pp(lines)

def findInd(data,index):
    for i,dtup in enumerate(data):
        idx,dta = dtup
        if idx == index:
            return i,dta

def rot1left(data,i):
    if i == 0:
        #return data[1:] + data[i:i+1], len(data)-1
        return data[1:-1] + [data[i]] + [data[-1]], len(data)-2
    elif i == (len(data) - 1):
        return data[0:i-1] + [data[i]] + [data[i-1]], i-1
    else:
        return data[0:i-1] + [data[i]] + [data[i-1]] + data[i+1:], i-1
    

def rot1right(data,i):
    if i == 0:
        return [data[1]] + [data[i]] + data[2:], i+1
    elif i == (len(data) - 1):
        #return [data[i]] + data[0:i], 0
        return [data[0]] + [data[i]] + data[1:i], 1
    else:
        return data[0:i] + [data[i+1]] + [data[i]] + data[i+2:], i+1
    
def rot(data,i,n):
    newi = i
    newdata = data[:]
    if n == 0:
        return newdata
    elif n < 0:
        for q in range(abs(n)):
            newdata,newi = rot1left(newdata,newi)
        return newdata
    else:
        for q in range(abs(n)):
            newdata,newi = rot1right(newdata,newi)
        return newdata


def rotFast(data,i,n):
    if n == 0:
        return data
    elif n < 0: # rotate left
        mag = abs(n)
        mag = mag % (len(data)-1)
        return rot(data,i,-mag)
    else: 
        mag = abs(n)
        mag = mag % (len(data)-1)
        return rot(data,i,mag)

def rotFast2(data,i,n):
    if n == 0:
        return data
    elif n < 0: # rotate left
        mag = abs(n)
        mag = mag % (len(data)-1)
        if mag == 0:
            return data
        val = data[i]
        d = data[0:i] + data[i+1:] # remove i
        newInd = i - mag
        if newInd < 0:
            newInd = len(d) + newInd # note this len is SMALLER than before we removed i
        if newInd == 0:
            return [val] + d[0:]
        return d[0:newInd] + [val] + d[newInd:]
    else: # rotate right
        mag = abs(n)
        mag = mag % (len(data)-1)
        if mag == 0:
            return data
        val = data[i]
        d = data[0:i] + data[i+1:] # remove i
        newInd = i + mag
        if newInd == len(d):
            return d + [val]
        elif newInd > len(d):
            newInd = newInd - len(d) # note this len is SMALLER than before we removed i
            return d[0:newInd] + [val] + d[newInd:]
        else:
            return d[0:newInd] + [val] + d[newInd:]

#pp(sorted(lines))
initial = tuple(lines)
indices = range(len(lines))
data = list(zip(indices,lines))
print()
for xxx in range(10):
    for ind in indices:
        
        i,d = findInd(data, ind)
        if d == 0:
            continue # nothing to do
        val = data[i]
        print(f"[{xxx}] {ind}/{len(indices)}  i={i}, d={d}, val={val}")
        # newLoc = i + d 
        # print(f"newLoc={newLoc}")
        # while newLoc < 0:
        #     newLoc = len(data) + 1 + newLoc 
        # while newLoc >= len(data):
        #     newLoc = newLoc - len(data)
        # print(f"adjusted newLoc={newLoc}")
        # data = data[0:i] + data[i+1:]
        # # if newLoc < i:
        # #     data = data[0:newLoc] + d + data[newLoc:]
        # # else:
        # #     data = data[0:newLoc]
        # data = data[0:newLoc] + [val] + data[newLoc:]
        datalen = len(data)
        #d1 = rot(data,i,d)
        #d2 = rotFast(data,i,d)
        data = rotFast2(data, i, d)
        # if d1 != d2:
        #     print(f"d1 != d2")
        #     #pp(d1)
        #     #pp(d2)
        # if d1 != data:
        #     print(f"d1 != data")
        # if d2 != data:
        #     print(f"d2 != data")
        datalen2 = len(data)
        if datalen != datalen2:
            print()
            print(f"#### ERROR datalen ({datalen}) != datalen2 ({datalen2})")
            print()
            time.sleep(5)
        #pp(data)
        #pp([val for idx,val in data])

# zero at 2387
# (4678, 9027)
# (1015, -543)
# (3321, -1480)
# result=7004

# zero at 2387
# (2938, 6906)
# (1015, -543)
# (3321, -1480)
# result=4883


zeroind = 0
for i,dtup in enumerate(data):
    if dtup[1] == 0:
        zeroind = i
        break
print(f"zero at {zeroind}")
index1 = (zeroind + 1000) % len(data)
index2 = (zeroind + 2000) % len(data)
index3 = (zeroind + 3000) % len(data)
print(data[index1])
print(data[index2])
print(data[index3])
result = data[index1][1] + data[index2][1] + data[index3][1]
print(f"result={result}")