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
    "A":1, # ROCK
    "X":1,
    "B":2, # PAPER 
    "Y":2,
    "C":3, # SCISSORS 
    "Z":3,
}

# what_to_play = {
#     "A":{
#         "X": ,# lose
#         "Y": ,# draw
#         "Z": ,# win
#     }
# }



outcome_scores = {
    "A":{ # Rock (opponent)
        "X":0+3, # lose, so scissors
        "Y":3+1, # draw, so rock
        "Z":6+2, # win, so paper
    },
    "B":{ # Paper (opponent)
        "X":0+1, # lose, so rock
        "Y":3+2, # draw, so paper
        "Z":6+3, # win, so scissors
    },
    "C":{ # Scissors (opponent)
        "X":0+2, # lose, so paper
        "Y":3+3, # draw, so scissors
        "Z":6+1, # win, so rock
    },
}

with open("input.txt","r") as f:
  data = [i.strip().split(" ") for i in f.readlines()] # .replace("X","A").replace("Y","B").replace("Z","C")

pp(data)
total_score = 0
for (opp,wl) in data:
    score = outcome_scores[opp][wl]
    #play = play_scores[you]
    #score = outcome + play
    total_score += score 
print(total_score)
