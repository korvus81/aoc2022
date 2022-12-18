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
from math import inf
import astar
import re

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)
COORD_MAX=4000000

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



# lines = ex 
# COORD_MAX = 20

pat = re.compile("Sensor at x=([-]?\d+), y=([-]?\d+): closest beacon is at x=([-]?\d+), y=([-]?\d+)")
#lines = [line_to_num_list_negs(l) for l in lines]

lines = [[int(x) for x in pat.match(l).groups()[0:4]] for l in lines]
pp(lines)


X = 0
Y = 1
minx = inf 
miny = inf 
maxx = -inf 
maxy = -inf 
sensors = set()
beacons = set()
for ln in lines:
    sensor = (ln[0],ln[1])
    beacon = (ln[2],ln[3])
    if ln[0] < minx:
        minx = ln[0]
    if ln[0] > maxx:
        maxx = ln[0]
    if ln[2] < minx:
        minx = ln[2]
    if ln[2] > maxx:
        maxx = ln[2]

    if ln[1] < miny:
        miny = ln[1]
    if ln[1] > maxy:
        maxy = ln[1]
    if ln[3] < miny:
        miny = ln[3]
    if ln[3] > maxy:
        maxy = ln[3]

    sensors.add(sensor)
    beacons.add(beacon)
if minx < 0:
    minx = 0
if miny < 0:
    miny = 0
if maxx > COORD_MAX:
    maxx = COORD_MAX
if maxy > COORD_MAX:
    maxy = COORD_MAX

# indexed by row
cant_be = [set() for i in range(COORD_MAX+1)]
can_be = [set() for i in range(COORD_MAX+1)]
can_be_coords = set()

def maybe_add(can_be_coords,x,y):
    if x >= 0 and y >= 0 and x <= COORD_MAX and y <=COORD_MAX and (x,y) not in beacons:
        can_be_coords.add((x,y))

def maybe_rem(can_be_coords,x,y):
    if x >= minx and y >= miny and x <= maxx and y <=maxy and (x,y) not in beacons:
        can_be_coords.discard((x,y)) # remove throws a KeyError

sensor_dist = []

for ln in lines:
    sensor = (ln[0],ln[1])
    beacon = (ln[2],ln[3])
    man_dist = abs(sensor[X]-beacon[X]) + abs(sensor[Y]-beacon[Y])
    sensor_dist.append((sensor[X],sensor[Y],man_dist))
    print(f"sensor={sensor}, beacon={beacon}, dist={man_dist}")
    maybe_add(can_be_coords,sensor[X],sensor[Y]-(man_dist+1))
    maybe_add(can_be_coords,sensor[X],sensor[Y]+(man_dist+1))
    for yval in range(sensor[Y]-man_dist,sensor[Y]+man_dist+1):
        #print(f" yval={yval}")
        sensor_dist_to_yval = abs(sensor[Y]-yval)
        xdist = man_dist - sensor_dist_to_yval
        maybe_add(can_be_coords,sensor[X]+(xdist+1),yval)
        maybe_add(can_be_coords,sensor[X]-(xdist+1),yval)
    print(f" (intermediate len of can_be_coords: {len(can_be_coords)} )")

print(f"len of can_be_coords: {len(can_be_coords)}")
num_to_check = len(can_be_coords)
still_can_be_coords = []
processed = 0
for (x,y) in can_be_coords:
    possible = True
    for (sens_x,sens_y,sens_dist) in sensor_dist:
        dist = abs(sens_x-x) + abs(sens_y-y)
        if dist <= sens_dist:
            possible = False
            break
    if possible:
        still_can_be_coords.append((x,y))
        print(f"can still be coords ({x},{y})")
        print(f"freq: {(x*4000000)+y}")
    processed += 1
    if processed % 100000 == 0:
        print(f"Processed {processed} - {100.0*processed/num_to_check:.2f}% done")
    
pp(still_can_be_coords)
