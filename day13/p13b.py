#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache,cmp_to_key
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

ex = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""".splitlines()

#lines = ex 

pp(lines)

# def parsePairs(lns):
#     pairs = [[]]
#     for ln in lns:
#         if len(ln.strip()) == 0:
#             pairs.append([])
#         else:
#             pairs[-1].append(eval(ln))
#     return pairs 

# pairs = parsePairs(lines)
# pp(pairs)

def parsePackets(lns):
    packets = []
    for ln in lns:
        if len(ln.strip()) == 0:
            pass
        else:
            packets.append(eval(ln))
    return packets 


#packets = parsePackets(lines)
packets = [eval(ln) for ln in lns if len(ln.strip()) > 0]
packets.append([[2]])
packets.append([[6]])

def compare(left,right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif right < left:
            return False
        else:
            return None
    elif type(left) == list and type(right) == list:
        for i in range(min(len(left),len(right))):
            res = compare(left[i],right[i])
            if res is True:
                return True
            elif res is False:
                return False 
            # must be None, which means continue
        # "If the left list runs out of items first, the inputs are in the right order."
        if len(left) < len(right): 
            return True
        if len(left) > len(right): 
            return False
        return None
    elif type(left) == list and type(right) == int:
        return compare(left, [right])
    elif type(left) == int and type(right) == list:
        return compare([left], right)
    else:
        print(f"ERROR type(left)={type(left)}, type(right)={type(right)}, left={left}, right={right}")
        return None

def compare_cmp(left, right):
    ret = compare(left,right)
    if ret is True:
        return -1
    elif ret is False:
        return 1
    else:
        return 0

# right_ind_sum = 0
# ind = 1
# for left,right in pairs:
#     print(f"=== Index {ind}")
#     pp(left)
#     pp(right)
#     res = compare(left,right)
#     print(res)
#     if res:
#         right_ind_sum += ind
#     print()
#     ind += 1

# print(right_ind_sum)

spackets = sorted(packets,key=cmp_to_key(compare_cmp))
pp(spackets)

div_packet_inds = []
for i,p in enumerate(spackets):
    if p == [[2]] or p == [[6]]:
        div_packet_inds.append(i+1) # 1-based indexes
pp(div_packet_inds)
print(div_packet_inds[0] * div_packet_inds[1])