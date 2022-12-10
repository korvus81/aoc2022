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

ex = """30373
25512
65332
33549
35390"""
#lines = [ln.strip() for ln in ex.splitlines()]

pp(lines)

data = [[int(r) for r in line] for line in lines]

for rownum,row in enumerate(data):
    for colnum,col in enumerate(row):
        if rownum == 23:
            if colnum == (len(row)-15):
                p(f"[green]{col}[/green]", end="")
            else:
                p(f"[red]{col}[/red]", end="")
        else:
            p(f"{col}", end="")
    print()
print()
#pp(data)


#pp(visible)

th_score = make2dList(0, len(data[0]), len(data))

for throw in range(1,len(data)-1): # skip edges, hence start at 1 and go to len-1
    for thcol in range(1,len(data[0])-1): # skip edges, hence start at 1 and go to len-1
        visible = make2dList(0, len(data[0]), len(data))
        thheight = data[throw][thcol]

        ### Look on same row
        row = throw
        
        score_right = 0
        for col in range(thcol+1, len(data[0])):
            score_right += 1
            if data[row][col] >= thheight:
                break
            
        
        score_left = 0
        for col in range(thcol-1,-1,-1):
            score_left += 1
            if data[row][col] >= thheight:
                break

            


        ### Look on same column
        col = thcol
        
        score_down = 0
        for row in range(throw+1,len(data)):
            score_down += 1
            if data[row][col] >= thheight:
                break

            

        score_up = 0
        for row in range(throw-1,-1,-1):
            score_up += 1
            if data[row][col] >= thheight:
                break

            
        print(f"({throw},{thcol}) left={score_left}, right={score_right}, down={score_down}, up={score_up}")
        th_score[throw][thcol] = score_right * score_left * score_down * score_up

pp([" ".join([("%03d" %c) for c in d]) for d in th_score])
total = max([max(row) for row in th_score])
print(total)