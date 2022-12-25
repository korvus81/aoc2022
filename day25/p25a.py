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

ex = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122""".splitlines()
#lines = ex 

pp(lines)



testdata = """        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0""".splitlines()
testdata = [(t[0:9].strip(),t[9:].strip()) for t in testdata]
pp(testdata)

def snafu_to_dec(sfu):
    #print(sfu)
    place = 1
    curval = 0
    for chi in range(len(sfu)-1,-1,-1):
        #print(chi, sfu[chi])
        match sfu[chi]:
            case "1":
                val = 1
            case "2":
                val = 2
            case "0":
                val = 0
            case "-":
                val = -1
            case "=":
                val = -2
            case other:
                print(f"ERROR, unknown char {sfu[chi]}")
        curval += val * place
        place = place * 5
    return curval

def to_base_5(num):
    digits = ""
    place = 1
    rem = num%5
    digits = str(rem) + digits
    num -= rem
    num = int(num / 5)
    while num > 0:
        rem = num%5
        digits = str(rem) + digits
        num -= rem
        num = int(num / 5)
    return digits

def dec_to_snafu(dec): # TODO
    
    b5 = "0"+to_base_5(dec)
    #print(f"dec={dec}   b5={b5}")
    sfu = ""
    carry = 0
    for chi in range(len(b5)-1,-1,-1):
        digit = int(b5[chi]) + carry
        #print(f"  digit {digit} sfu='{sfu}'")
        match digit:
            case 0|1|2:
                sfu = str(digit) + sfu
                carry = 0
            case 3:
                sfu = "=" + sfu
                carry = 1
            case 4:
                sfu = "-" + sfu
                carry = 1
            case 5: # only can happen from carry
                sfu = "0" + sfu
                carry = 1
            case other:
                print(f"UNKNOWN STATE digit={digit}")
    return sfu.lstrip("0")



for dec,sfu in testdata:
    d = snafu_to_dec(sfu)
    if d != int(dec):
        print(f"failed snafu_to_dec, input={sfu}, output={d}, expected output={dec}")
    print()
    s = dec_to_snafu(int(dec))
    if s != sfu:
        print(f"failed dec_to_snafu, input=`{dec}`, output=`{s}`, expected output=`{sfu}`")

total = 0
for ln in lines:
    d = snafu_to_dec(ln.strip())
    total += d 
print(total)
print(dec_to_snafu(total))