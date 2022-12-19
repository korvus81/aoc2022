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
import re

from util import *
from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
lines = list(lns)

ex = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()
#lines = ex

TIME_LIMIT=24
RESOURCE_TYPES=["ore","clay","obsidian","geode"]

pp(lines)


pat = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
lines = [pat.match(l).groups() for l in lines]
blueprints = {int(l[0]):{"ore":{"ore":int(l[1])}, "clay":{"ore":int(l[2])}, "obsidian":{"ore":int(l[3]),"clay":int(l[4])}, "geode":{"ore":int(l[5]), "obsidian":int(l[6])} } for l in lines}
pp(blueprints)

def num_geodes(blueprint, time_left,resources,robots):
    if time_left == 0:
        return resources["geode"],[]
    new_resources = {r:num for r,num in robots.items()}
    # we will start with building one robot type at a time, but may need to do several
    possible_robot_to_build = None
    possible_robots_to_build = []
    rob_order =  ["geode","obsidian","clay","ore"]

    
    # should I build obsidian?
    ob = resources["obsidian"]
    ob_with_new_robot = ob
    robot_matters = False
    new_geode_bots = 0
    new_geode_bots_with_new_ob_bot = 0
    for i in range(time_left):
        ob += robots["obsidian"]
        ob_with_new_robot += (robots["obsidian"]+1)
        if ob > blueprint["geode"]["obsidian"]:
            ob -= blueprint["geode"]["obsidian"]
            new_geode_bots += 1
        if ob_with_new_robot > blueprint["geode"]["obsidian"]:
            ob_with_new_robot -= blueprint["geode"]["obsidian"]
            new_geode_bots_with_new_ob_bot += 1
        if new_geode_bots < new_geode_bots_with_new_ob_bot:
            robot_matters = True
    if not robot_matters:
        rob_order.remove("obsidian")
        #rob_order = ["geode","clay","ore"] # skip obsidian
    

    # should I build clay?
    clay= resources["clay"]
    clay_with_new_robot = ob
    robot_matters = False
    new_obs_bots = 0
    new_obs_bots_with_new_ob_bot = 0
    for i in range(time_left):
        clay+= robots["clay"]
        clay_with_new_robot += (robots["clay"]+1)
        if clay> blueprint["obsidian"]["clay"]:
            clay-= blueprint["obsidian"]["clay"]
            new_obs_bots += 1
        if clay_with_new_robot > blueprint["obsidian"]["clay"]:
            clay_with_new_robot -= blueprint["obsidian"]["clay"]
            new_obs_bots_with_new_ob_bot += 1
        if new_obs_bots < new_obs_bots_with_new_ob_bot:
            robot_matters = True
    if not robot_matters:
        rob_order.remove("clay")
        #rob_order = ["geode","clay","ore"] # skip obsidian
    
    max_ore_needed = max([bp.get("ore",0) for bp in blueprint.values()])
    if max_ore_needed*time_left <= resources["ore"]+(robots["ore"]*time_left):
        rob_order.remove("ore")



    # if robots["clay"] == 0:
    #     rob_order =  ["geode","obsidian","clay"]
    # else:
    #     rob_order = ["geode","obsidian","ore","clay"]
    for robot_type in rob_order: # ["geode","obsidian","clay","ore"]:#RESOURCE_TYPES[::-1]:
        robot_bp = bp[robot_type]
        if robot_type == "ore" and time_left <= robot_bp["ore"]:
            continue # if it takes N ore to build an ore robot, you need N more cycles just to break even
        if robot_type == "clay" and time_left <= 3:
            continue # new clay can make new obsidian robots in one cycle, and new obsidian robots can make new geode robots in a cycle, so we need 3 cycles to make anything

        possible = True
        for res,qty_to_build in robot_bp.items():
            if resources[res] < qty_to_build:
                possible = False
        if possible:
            if possible_robot_to_build is None:
                possible_robot_to_build = robot_type
            possible_robots_to_build.append(robot_type)
    
    # update resources
    for r in RESOURCE_TYPES:
        resources[r] += new_resources[r]
    
    #if time_left > 20 or time_left==4:
    #    print(f"[{time_left}] resources={resources} robots={robots} possible_robots_to_build={possible_robots_to_build}")
    #time.sleep(0.01)
    geode_amounts = []
    
    # it's important, maybe we can take this short-circuit?
    if "geode" in possible_robots_to_build:
        possible_robots_to_build = ["geode"]
    # option: build each robot type
    #if possible_robot_to_build is not None:
    #    p = possible_robot_to_build
    for p in possible_robots_to_build:
        r2 = resources.copy()
        for res,num in blueprint[p].items():
            r2[res] -= num
        ro = robots.copy()
        ro[p] += 1
        g,path = num_geodes(blueprint, time_left-1, r2, ro)
        #pp((g,path))
        geode_amounts.append((g,path))
    
    # can we do all of them?
    # if len(possible_robots_to_build) > 1:
    #     total_cost = {res:0 for res in RESOURCE_TYPES}
    #     for p in possible_robots_to_build:
    #         robot_bp = blueprint[p]
    #         for res,cnt in robot_bp.items():
    #             total_cost[res] += cnt
    #     possible = True
    #     for res,cnt in total_cost.items():
    #         if resources[res] < cnt:
    #             possible = False
    #     if possible:
    #         r2 = resources.copy()
    #         for res,num in total_cost.items():
    #             r2[res] -= num
    #         ro = robots.copy()
    #         for p in possible_robots_to_build:
    #             ro[p] += 1
    #         g,path = num_geodes(blueprint, time_left-1, r2, ro)
    #         geode_amounts.append((g,path))
    # option: do nothing -- only do this if there are robots we can't build now
    #if len(possible_robots_to_build) < 4:
    # if we have enough ore to build anything and had some options to build, skip the empty case
    if len(possible_robots_to_build) == 0 or max_ore_needed > resources["ore"]:
        g,path = num_geodes(blueprint, time_left-1, resources.copy(), robots.copy())
        #(g,path)
        geode_amounts.append((g,path))
    geode_amounts.sort(key=lambda x:x[0])
    #pp(geode_amounts)
    geode_amt_to_return = geode_amounts[-1][0]
    path_to_return = geode_amounts[-1][1]
    path_to_return = path_to_return.copy()
    path_to_return.append(f"[{time_left}] resources={resources} robots={robots} possible_robots_to_build={possible_robots_to_build}")
    return geode_amt_to_return,path_to_return




def num_can_build(robot_bp, resources):
    num = 0
    tmp_resources = resources.copy()
    possible = True
    if possible: # was while, but changed to if to run only once
        for res,qty_to_build in robot_bp.items():
            if tmp_resources[res] < qty_to_build:
                possible = False
        if possible:
            num += 1
            for res,qty_to_build in robot_bp.items():
                tmp_resources[res] -= qty_to_build
    return num,tmp_resources

def num_geodes2(blueprint, time_left,resources,robots):
    if time_left == 0:
        return resources["geode"],[]
    new_resources = {r:num for r,num in robots.items()}
    # we will start with building one robot type at a time, but may need to do several
    possible_robot_to_build = None
    possible_robots_to_build = []


    rob_order =  ["geode","obsidian","clay","ore"]
    
    # should I build obsidian?
    ob = resources["obsidian"]
    ob_with_new_robot = ob
    robot_matters = False
    new_geode_bots = 0
    new_geode_bots_with_new_ob_bot = 0
    for i in range(time_left):
        ob += robots["obsidian"]
        ob_with_new_robot += (robots["obsidian"]+1)
        if ob > blueprint["geode"]["obsidian"]:
            ob -= blueprint["geode"]["obsidian"]
            new_geode_bots += 1
        if ob_with_new_robot > blueprint["geode"]["obsidian"]:
            ob_with_new_robot -= blueprint["geode"]["obsidian"]
            new_geode_bots_with_new_ob_bot += 1
        if new_geode_bots < new_geode_bots_with_new_ob_bot:
            robot_matters = True
    if not robot_matters:
        rob_order.remove("obsidian")
        #rob_order = ["geode","clay","ore"] # skip obsidian
    

    # should I build clay?
    clay= resources["clay"]
    clay_with_new_robot = ob
    robot_matters = False
    new_obs_bots = 0
    new_obs_bots_with_new_ob_bot = 0
    for i in range(time_left):
        clay+= robots["clay"]
        clay_with_new_robot += (robots["clay"]+1)
        if clay> blueprint["obsidian"]["clay"]:
            clay-= blueprint["obsidian"]["clay"]
            new_obs_bots += 1
        if clay_with_new_robot > blueprint["obsidian"]["clay"]:
            clay_with_new_robot -= blueprint["obsidian"]["clay"]
            new_obs_bots_with_new_ob_bot += 1
        if new_obs_bots < new_obs_bots_with_new_ob_bot:
            robot_matters = True
    if not robot_matters:
        rob_order.remove("clay")
        #rob_order = ["geode","clay","ore"] # skip obsidian
    
    max_ore_needed = max([bp.get("ore",0) for bp in blueprint.values()])
    if max_ore_needed*time_left <= resources["ore"]+(robots["ore"]*time_left):
        rob_order.remove("ore")


    # if robots["clay"] == 0:
    #     rob_order =  ["geode","obsidian","clay"]
    # else:
    #     rob_order = ["geode","obsidian","ore","clay"]
    total_new_robots = 0 # just for me to watch
    robots_can_build = {r:0 for r in RESOURCE_TYPES}
    running_resources = resources.copy()
    for robot_type in rob_order: # ["geode","obsidian","clay","ore"]:#RESOURCE_TYPES[::-1]:
        if total_new_robots == 0: # temporarily only build one
            robot_bp = bp[robot_type]
            num,running_resources = num_can_build(robot_bp, running_resources)
            robots_can_build[robot_type] += num
            total_new_robots += num

    r2 = resources.copy()
    ro = robots.copy()
    if total_new_robots > 0:
        r2 = running_resources
        for r,num in robots_can_build.items():
            ro[r] += num
    # update resources
    for r in RESOURCE_TYPES:
        resources[r] += new_resources[r]
        r2[r] += new_resources[r]
    
    #if time_left > 20 or time_left==4:
    #    print(f"[{time_left}] resources={resources} robots={robots} possible_robots_to_build={possible_robots_to_build}")
    #time.sleep(0.01)
    geode_amounts = []
    
    if total_new_robots > 0:
        g,path = num_geodes2(blueprint, time_left-1, r2, ro)
        geode_amounts.append((g,path))
    
    g,path = num_geodes2(blueprint, time_left-1, resources.copy(), robots.copy())
    geode_amounts.append((g,path))

    geode_amounts.sort(key=lambda x:x[0])
    #pp(geode_amounts)
    geode_amt_to_return = geode_amounts[-1][0]
    path_to_return = geode_amounts[-1][1]
    path_to_return = path_to_return.copy()
    path_to_return.append(f"[{time_left}] resources={resources} robots={robots} robots_can_build={robots_can_build}")
    return geode_amt_to_return,path_to_return




def can_build(robot_bp, resources):
    possible = True
    for res,qty_to_build in robot_bp.items():
        if resources[res] < qty_to_build:
            possible = False
    return possible

def resources_after_build(robot_bp, resources):
    tmp_resources = resources.copy()
    for res,qty_to_build in robot_bp.items():
        tmp_resources[res] -= qty_to_build
    return tmp_resources

def quality_score(state):
    minute,resources,mined,robots = state
    return  10 * (mined["clay"]+ 10 * (mined["obsidian"]+(10*mined["geode"]))) + mined["ore"] 

# lets try BFS...
def num_geodes3(blueprint):
    states = []
    robots = {r:0 for r in RESOURCE_TYPES}
    robots["ore"] = 1
    resources = {r:0 for r in RESOURCE_TYPES}
    mined = {r:0 for r in RESOURCE_TYPES}
    cur_min = 0
    state = (cur_min,resources,mined,robots) # time, 
    states.append(state)
    max_geodes_mined = 0
    
    while len(states) > 0:
        minute,resources,mined,robots = states.pop(0)
        if minute == TIME_LIMIT:
            max_geodes_mined = max(max_geodes_mined,mined["geode"])
            continue # terminal state

        if minute > cur_min:
            states.sort(key=quality_score,reverse=True)
            states = states[:10000]
            cur_min = minute


        new_mined = mined.copy()
        new_resources = resources.copy() # this will be after mining, but can't use these to build robots
        for robot_type in RESOURCE_TYPES:
            new_mined[robot_type] += robots[robot_type]
            new_resources[robot_type] += robots[robot_type]
        
        for robot_type in RESOURCE_TYPES:
            if can_build(blueprint[robot_type],resources): # old resources here
                ro = robots.copy()
                ro[robot_type] += 1
                ns = (minute+1,resources_after_build(blueprint[robot_type],new_resources), new_mined, ro)
                states.append(ns)
        # no build case
        ns = (minute+1,new_resources, new_mined, robots)
        states.append(ns)
    return max_geodes_mined

qualities = []
for bpnum,bp in blueprints.items():
    time_left = TIME_LIMIT
    robots = {r:0 for r in RESOURCE_TYPES}
    robots["ore"] = 1
    resources = {r:0 for r in RESOURCE_TYPES}
    #g,path = num_geodes(bp, time_left, resources, robots)
    g = num_geodes3(bp)
    quality = bpnum * g
    pp(bp)
    print(f"bpnum={bpnum}, geodes={g}, quality={quality}")
    #pp(path)
    qualities.append(quality)
    print()
pp(qualities)
print(sum(qualities))





# That's not the right answer; your answer is too low. If you're stuck, make sure you're using the full input data; there are also some general tips on the about page, or you can ask for hints on the subreddit. Please wait one minute before trying again. (You guessed 1345.) [Return to Day 19]