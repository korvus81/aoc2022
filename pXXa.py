#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
from sys import exit
from collections import defaultdict,namedtuple
import time

from aocd import lines  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data


def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]

pp(lines)
