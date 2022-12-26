import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
from math import nan

test_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


##data = test_data.splitlines()
data = test_data.strip()

with open('day17_input.txt', 'r') as f:
    data = f.read().strip()


def rock(n, L, B):
    if n == 0:
        return [(L, B), (L+1, B), (L+2, B), (L+3, B)]
    elif n == 1:
        return [(L, B+1), (L+1, B+2), (L+1, B+1), (L+1, B), (L+2, B+1)]
    elif n == 2:
        return [(L+2, B+2), (L+2, B+1), (L, B), (L+1, B), (L+2, B)]
    elif n == 3:
        return [(L, B+3), (L, B+2), (L, B+1), (L, B)]
    elif n == 4:
        return [(L, B+1), (L+1, B+1), (L, B), (L+1, B)]



ri = 0      # Rock Index
ji = 0      # Jet Index
h = 0       # Current tower height
grid_height = 2023 * 5
grid_height = 50455
grid = np.zeros( (grid_height, 7) )     # The grid will be upside down for indexing convenience


C = {0:' ', 1:'#', 2:'@'}
def draw(L, B):
    rock_squares = rock(ri, L, B)
    for ix in range(h+6, -1, -1):
        row = grid[ix,:]
        line = '|'
        for (jx, x) in enumerate(row):
            if (jx, ix) in rock_squares:
                line += '@'
            else:
                if ix == h-1:
                    if x == 0:
                        line += '-'
                    else:
                        line += C[x]
                else:
                    line += C[x]
        print(line + '|')
    print('+-------+\n')


J = {'<':-1, '>':1}

n_rocks = 10000

H = [0] * n_rocks

for n_rock in range(n_rocks):

    if not n_rock % 1000:
        print(n_rock, '/', n_rocks)

    (L, B) = 2, h + 3

    falling = True
    while falling:

        # JET
        jet = data[ji]
        ji = (ji + 1) % len(data)

        jet_move = rock(ri, L + J[jet], B)
        
        if any([xy[0] < 0 or xy[0] > 6 for xy in jet_move]):
            pass
        elif any([grid[y,x] for (x,y) in jet_move]):
            pass
        else:
            L += J[jet]

        # FALL
        fall_move = rock(ri, L, B - 1)
        if any([xy[1] < 0 for xy in fall_move]) or any([grid[y,x] for (x,y) in fall_move]):
            falling = False
            for (x,y) in rock(ri, L, B):
                grid[y,x] = 1
                for hi in range(grid_height):
                    if any(grid[hi,:]):
                        continue
                    h = hi
                    break
            pass
        else:
            B -= 1

    H[n_rock] = h
    ri = (ri + 1) % 5


##print(H)
deltas = np.diff(H)
##print(deltas)




# deltas is eventually periodic.
# We start from the end and work our way backward, looking for a full repeat.

deltas = np.flip(deltas)
for n in range(6, len(deltas)//4):
    P = deltas[:n]
    if all([x == y for (x, y) in zip(deltas[n:2*n], P)]): #pattern found
        print('found')
        break

target = 1000000000000

P = np.flip(P)
deltas = np.flip(deltas)

print('Growth of', sum(P), 'every', len(P), 'rocks')
print('Current height is', h, 'after', n_rock+1, 'rocks')
further_repeats = (target - n_rock - 1) // len(P)
remainder = (target - n_rock - 1) % len(P)
print('To reach', target, 'rocks, pattern repeats', further_repeats, 'times, rem', remainder)
further_growth = int(sum(P)) * int(further_repeats) + int(sum(P[:remainder]))
print('For a final height of', h + further_growth)









