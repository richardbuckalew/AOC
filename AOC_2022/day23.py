import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
from time import time

test_data = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""


data = test_data.splitlines()

##with open('day23_input.txt', 'r') as f:
##    data = f.readlines()


N = np.array([-1, 0])
S = np.array([1, 0])
E = np.array([0, 1])
W = np.array([0, -1])

NE = N + E
NW = N + W
SE = S + E
SW = S + W


class Elf:
    def __init__(self, xy):
        self.xy = xy
        self.proposal = None


def parse_data(data):
    xmin = 0
    xmax = len(data)
    ymin = 0
    ymax = max([len(line) for line in data])

    E = []

    for (i, line) in enumerate(data):
        for (j, c) in enumerate(line):
            if c == '#':
                E.append(Elf(np.array((i,j))))
    
    return (E, xmin, xmax, ymin, ymax)

def draw(D):
    xmin = min([xy[0] for xy in D])
    xmax = max([xy[0] for xy in D])+1
    ymin = min([xy[1] for xy in D])
    ymax = max([xy[1] for xy in D])+1
    for i in range(xmin, xmax):
        s = ''
        for j in range(ymin, ymax):
            if (i,j) in D:
                s += '#'
            else:
                s += '.'
        print(s)
    print('\n')
            
def empty(E, xmin, xmax, ymin, ymax):
    return (xmax - xmin) * (ymax - ymin) - len(E)



(EE, xmin, xmax, ymin, ymax) = parse_data(data)
DD = {tuple(e.xy):e for e in EE}
draw(DD)

dirs = [N, S, W, E]
quads = [[NW, N, NE], [SW, S, SE], [SW, W, NW], [SE, E, NE]]
ring = [N, S, W, E, NE, NW, SW, SE]



n_rounds = 10

for n_round in range(n_rounds):
    DD = {tuple(e.xy):e for e in EE}

    for e in EE:
        e.proposal = None
        has_neighbors = False
        for d in ring:
            if tuple(e.xy + d) in DD:
                has_neighbors = True
                break
        if has_neighbors:
            for (cd, quad) in zip(dirs, quads):
                if any([tuple(e.xy + d) in DD for d in quad]):
                    continue
                e.proposal = e.xy + cd
                break

    P = defaultdict(int)
    for e in EE:
        if e.proposal is not None:
            P[tuple(e.proposal)] += 1

    for e in EE:
        if e.proposal is not None:
            if P[tuple(e.proposal)] == 1:
                e.xy = np.copy(e.proposal)
##                print('.', end = '')
##    print('')

    dirs.append(dirs.pop(0))
    quads.append(quads.pop(0))


    DD = {tuple(e.xy):e for e in EE}
    print('Round', n_round+1)
    draw(DD)
    


xmin = min([xy[0] for xy in DD])
xmax = max([xy[0] for xy in DD])+1
ymin = min([xy[1] for xy in DD])
ymax = max([xy[1] for xy in DD])+1
print(empty(EE, xmin, xmax, ymin, ymax))





        
        
        
        














