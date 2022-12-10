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

# example
# lines = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2""".splitlines()



pp(lines)

data = [(x1,int(x2)) for (x1,x2) in [ln.split() for ln in lines]]
pp(data)

def touching(p1,p2):
    #  equal          x is same, y is +/- 1 
    #if p1 == p2 or (p1[0] == p2[0] and abs(p1[1]-p2[1]) <= 1) or (p1[1] == p2[1] and abs(p1[0]-p2[0]) <= 1) or (p1[1])
    if (abs(p1[0]-p2[0]) <= 1 and abs(p1[1]-p2[1]) <= 1):
        return True
    return False

def printboard(start,visited):
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    for v in visited:
        if v[0] < minx:
            minx = v[0]
        if v[0] > maxx:
            maxx = v[0]
        if v[1] < miny:
            miny = v[1]
        if v[1] > maxy:
            maxy = v[1]
    for y in range(maxy,miny-1,-1):
        for x in range(minx,maxx+1):
            if (x,y) == start:
                print("s",end="")
            elif (x,y) in visited:
                print("#",end="")
            else:
                print(".",end="")
        print()

start = (0,0) # x,y
head = (0,0)
tail = (0,0)
visited = set()
visited.add(tail)
for direction,cnt in data:
    for i in range(cnt):
        match direction:
            case "U":
                head = (head[0],head[1]+1)
            case "D":
                head = (head[0],head[1]-1)
            case "L":
                head = (head[0]-1,head[1])
            case "R":
                head = (head[0]+1,head[1])
        if not touching(head,tail):
            if head[0] == tail[0]:
                if head[1] > tail[1]:
                    tail = (tail[0], tail[1]+1)
                else:
                    tail = (tail[0], tail[1]-1)
            elif head[1] == tail[1]:
                if head[0] > tail[0]:
                    tail = (tail[0]+1, tail[1])
                else:
                    tail = (tail[0]-1, tail[1])
            else:
                xdir = 1 if head[0] > tail[0] else -1
                ydir = 1 if head[1] > tail[1] else -1
                tail = (tail[0]+xdir,tail[1]+ydir)
        #pp(tail)
        visited.add(tail)
pp(visited)
printboard(start,visited)

print(len(visited))
                
