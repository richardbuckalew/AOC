import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
from math import nan
from time import time

test_data = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


##data = test_data.splitlines()

with open('day19_input.txt', 'r') as f:
    data = f.readlines()




def parse_data(data):
    blueprints = []
    for (n,line) in enumerate(data):
        B = []
        s = line.split(':')[-1].split('.')
        for (ix, robot_type) in enumerate(s):
            words = robot_type.split()
            if words:
                c = np.zeros(4, int)
                c[0] = int(words[4])
                if ix == 2:
                    c[1] = int(words[7])
                elif ix == 3:
                    c[2] = int(words[7])
                B.append(c.copy())
        blueprints.append(B.copy())
    return blueprints
            
blueprints = parse_data(data)
T = 32
known_order = [1, 1, 1, 2, 1, 2, 3, 3]


"""Returns the robot vector, resource vector, and time of the state
immediately after building a robot of type r at the beginning of round t
using blueprint B. If the robot cannot be built, returns None."""
def future_state(t, r, robots, resources, B):
    if r == 2 and robots[1] == 0:
        return None
    if r == 3 and robots[2] == 0:
        return None             # impossible to build
    cost = B[r]
    new_resources = resources.copy()
    dt = 1                      # earliest possible is next turn
    while any(np.greater(cost, new_resources)):
        new_resources += robots
        dt += 1
    if t + dt >= T:
        return None
    new_resources += robots - cost  # we'll earn resources this turn regardless
    new_robots = robots.copy()
    new_robots[r] += 1
    return (new_robots, new_resources, t+dt)


def build_path(t, path, robots, resources, B):
    future_values = []
    for r in range(3, -1, -1):
        if (r < 3) and (robots[r] * (T-t) + resources[r] >= (max([c[r] for c in B]) * (T-t))):
            continue
        x = future_state(t, r, robots, resources, B)
        if x:
            future_values.append(build_path(x[2], path+[r], x[0], x[1], B))
    if future_values:
        return max(future_values, key = lambda x:x[0])
    else:
        return ((resources + (T-t)*robots)[3], path)


# assumption: each robot built is built as soon as possible
# consequence: we can map directly from build to build rather
#   than modeling in-between states explicitly
# conclusion: the state space consists only of robot vectors at
#   each possible time. We need only mark the times at which
#   geode bots are built in each path.


q_tot = 1

for (ib, B) in enumerate(blueprints[:3]):

    print(ib+1, ': ', end = '')
    for b in B:
        print(b, '  ', end = '')
    print('')
    
    robots = np.array([1, 0, 0, 0])
    resources = np.zeros_like(robots)
    tt = time()
    
    x = build_path(0, [], robots, resources, B)

    
    print('   ', x, '  (', time() - tt, ')')
    q_tot *= x[0]
        

print('total:', q_tot)
    
    














