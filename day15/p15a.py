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
yval = 2000000


ex = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()



#lines = ex 
#yval = 10


lines = [line_to_num_list(l) for l in lines]

pp(lines)


X = 0
Y = 1
beacons = set()
for ln in lines:
    beacon = (ln[2],ln[3])
    beacons.add(beacon)


cant_be = set()
cant_be_x = set()
for ln in lines:
    sensor = (ln[0],ln[1])
    beacon = (ln[2],ln[3])
    man_dist = abs(sensor[X]-beacon[X]) + abs(sensor[Y]-beacon[Y])
    print(f"sensor={sensor}, beacon={beacon}, dist={man_dist}")
    sensor_dist_to_yval = abs(sensor[Y]-yval)
    xdist = man_dist - sensor_dist_to_yval
    if xdist >= 0:
        if (sensor[X],yval) not in beacons:
            cant_be.add((sensor[X],yval)) # directly above/below sensor
            cant_be_x.add(sensor[X])
            #print(f"{sensor[X]}",end=" ")
        for i in range(1,xdist+1):
            if (sensor[X]-i,yval) not in beacons:
                cant_be.add((sensor[X]-i,yval))
                cant_be_x.add(sensor[X]-i)
                #print(f"{sensor[X]-i}",end=" ")
            if (sensor[X]+i,yval) not in beacons:
                cant_be.add((sensor[X]+i,yval))
                cant_be_x.add(sensor[X]+i)
                #print(f"{sensor[X]+i}",end=" ")
    print()

print("answers:")
print(len(cant_be),len(cant_be_x))
#pp(sorted(cant_be_x))
