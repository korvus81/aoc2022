#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time

def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]

play_scores = {
    "A":1,
    "X":1,
    "B":2,
    "Y":2,
    "C":3,
    "Z":3,
}

outcome_scores = {
    "A":{ # Rock (opponent)
        "A":3, # Rock - draw
        "B":6, # Paper - win
        "C":0, # Scissors - lose
    },
    "B":{ # Paper (opponent)
        "A":0, # Rock - lose
        "B":3, # Paper - draw
        "C":6, # Scissors - win
    },
    "C":{ # Scissors (opponent)
        "A":6, # Rock - win
        "B":0, # Paper - lose
        "C":3, # Scissors - draw
    },
}

with open("input.txt","r") as f:
  data = [i.strip().replace("X","A").replace("Y","B").replace("Z","C").split(" ") for i in f.readlines()]

pp(data)
total_score = 0
for (opp,you) in data:
    outcome = outcome_scores[opp][you]
    play = play_scores[you]
    score = outcome + play
    total_score += score 
print(total_score)
