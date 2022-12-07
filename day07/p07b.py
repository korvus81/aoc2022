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



sample = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

#lines = [s.strip() for s in sample.splitlines()]

pp(lines)


filesystem_size = 70000000
space_needed = 30000000

count_size_max = 100000

# returns (size, [(dir,size)])
def recurse(curdir):
    dir_sizes = []
    cur_size = 0
    for k in curdir.keys():
        if type(curdir[k]) == int:
            cur_size+=curdir[k]
        elif type(curdir[k]) == dict:
            s,dirs = recurse(curdir[k])
            dir_sizes.append( (k,s) )
            for d in dirs:
                dir_sizes.append( (k+"/"+d[0],d[1]) )
            cur_size += s
        else:
            print(f"unknown type for key {k} = {type(curdir[k])}")
    p(f"returning {(cur_size, dir_sizes)}")
    return (cur_size, dir_sizes)


filesystem = {}

file_collection = []
in_ls = True

curdir = []

for l in lines:
    if l.startswith("$ cd "):
        dir = l.replace("$ cd ","")
        if dir == "/":
            curdir = []
        elif dir == "..":
            curdir = curdir[:-1]
        else:
            curdir.append(dir)
    elif l.startswith("$ ls"):
        file_collection = []
        in_ls = True
    elif in_ls:
        size,name = l.split(" ")
        if size == "dir":
            pass
        else:
            print(f"file {name} @ {size}")
            d = filesystem
            for c in curdir:
                print(f"Going into {c}...")
                if c not in d:
                    d[c] = {}
                d = d[c]
            d[name] = int(size)
    else:
        print(f"ERROR - no idea what to do with `{l}`!!")
        time.sleep(1)
p(filesystem)
sz, dir_sizes = recurse(filesystem)
print(f"total size: {sz}")
pp(dir_sizes)
total_size = 0
for d in dir_sizes:
    total_size += d[1]
print(total_size)

free_space = filesystem_size - sz
min_dir_size_to_delete = space_needed - free_space
print(f"looking for at least {min_dir_size_to_delete}...")
dirs = [(dirname,sz) for (dirname,sz) in dir_sizes if sz >= min_dir_size_to_delete]
dirs = sorted(dirs, key=lambda x:x[1])
pp(dirs)
