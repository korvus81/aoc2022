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
import itertools
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

pp(lines)

seqlength = 14

st = lines[0].strip()
buffer = []
for i,ch in enumerate(st):
    buffer.append(ch)
    if len(buffer) > seqlength:
        buffer = buffer[-seqlength:]
    pp(buffer)
    match = False
    for c in list(itertools.combinations(buffer,2)):
        if c[0] == c[1]:
            match = True
    if not match and len(buffer) == seqlength:
        pp(buffer)
        print(i+1) # i is zero-based
        break
    #if buffer[0] != buffer[1] != buffer[2]