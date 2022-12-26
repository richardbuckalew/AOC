import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
from math import nan

test_data = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def nbrs(x,y,z):
    return [(x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)]


##data = test_data.splitlines()

with open('day18_input.txt', 'r') as f:
    data = f.readlines()


D = {}      # keys: cube coords. values: neighboring cubes


for line in data:
    xyz = tuple([int(a) for a in line.split(',')])
    D[xyz] = []
    for nbr in nbrs(*xyz):
        if nbr in D:
            D[xyz].append(nbr)
            D[nbr].append(xyz)

all_faces = 0
for (k, v) in D.items():
    all_faces += 6 - len(v)

print('Part 1:', all_faces)




# bbox
LL = tuple((min([xyz[i]-1 for xyz in D]) for i in [0,1,2]))
UU = tuple((max([xyz[i]+1 for xyz in D]) for i in [0,1,2]))


# inverse boxes - these are the 'air' cubes
air = {}
for x in range(LL[0], UU[0]+1):
    for y in range(LL[1], UU[1]+1):
        for z in range(LL[2], UU[2]+1):
            if (x,y,z) not in D:
                air[(x,y,z)] = []
                for nbr in nbrs(x,y,z):
                    if nbr in air:
                        air[nbr].append((x,y,z))
                        air[(x,y,z)].append(nbr)


# find the air cubes which are not connected to the outside
# by partitioning the graph using a graph traversal. discard
# all components containing known exterior points. Count faces
# on what remains and subtract from part 1.

flat_list = list(air.keys())
components = [0 for xyz in flat_list]
c_dict = defaultdict(list)

nc = 1
while not all(components):
    ix = components.index(0)
    Q = [flat_list[ix]]
    components[ix] = nc
    c_dict[nc] = [Q[-1]]

    while Q:
        (x,y,z) = Q.pop(0)
        for nbr in nbrs(x,y,z):
            if nbr in air:
                jx = flat_list.index(nbr)
                if not components[jx]:
                    components[jx] = nc
                    c_dict[nc].append(nbr)
                    Q.append(nbr)

    nc += 1

outside_component = components[flat_list.index(LL)]

for n_component in range(2, max(components)+1):
    for xyz in c_dict[n_component]:
        all_faces -= (6 - len(air[xyz]))

print('Part 2:', all_faces)
    

















    
