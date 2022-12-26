import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
from time import time

test_data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


##data = test_data.splitlines()

with open('day22_input.txt', 'r') as f:
    data = f.readlines()

def parse_data(data):
    steps = data.pop(-1)
    data = data[:-1]

    H = len(data)
    W = max([len(line) for line in data])
    block_size = W // 3

    grid = np.zeros((H, W), int)

    for (i, line) in enumerate(data):
        for (j, c) in enumerate(line):
            if c == ' ':
                grid[i,j] = 0
            elif c == '.':
                grid[i,j] = 1
            elif c == '#':
                grid[i,j] = 2
##            else:
##                raise(ValueError('unknown tile: ' + c))
    
    return (grid, steps, block_size)

CW = np.array([[0, 1], [-1, 0]])
CCW = np.array([[0, -1], [1, 0]])
        




(grid, steps, block_size) = parse_data(data)
(H, W) = grid.shape

ix = 0
for j in range(W):
    if grid[0,j] == 1:
        jy = j
        break

x = np.array([ix, jy])
v = np.array([0,1])         #initially facing right
path = {(ix, jy):'>'}


C = {0:' ', 1:'.', 2:'#'}
def draw():
    for i in range(H):
        s = ''
        for j in range(W):
            if (i,j) in path:
                s += path[(i,j)]
            else:
                s += C[grid[i,j]]
        print(s)
    print('\n')

def arrow(v):
    if v[0] > 0:
        return 'v'
    elif v[0] < 0:
        return '^'
    elif v[1] > 0:
        return '>'
    else:
        return '<'

##draw()



left1 = [(i, block_size) for i in range(block_size)]
left3 = [(i, block_size) for i in range(block_size, 2*block_size)]
left4 = [(i, 0) for i in range(2*block_size, 3*block_size)]
left6 = [(i, 0) for i in range(3*block_size, 4*block_size)]
right2 = [(i, 3*block_size-1) for i in range(block_size)]
right3 = [(i, 2*block_size-1) for i in range(block_size, 2*block_size)]
right5 = [(i, 2*block_size-1) for i in range(2*block_size, 3*block_size)]
right6 = [(i, block_size-1) for i in range(3*block_size, 4*block_size)]
top1 = [(0,i) for i in range(block_size, 2*block_size)]
top2 = [(0, i) for i in range(2*block_size, 3*block_size)]
top4 = [(2*block_size, i) for i in range(block_size)]
bottom2 = [(block_size-1, i) for i in range(2*block_size, 3*block_size)]
bottom5 = [(3*block_size-1, i) for i in range(block_size, 2*block_size)]
bottom6 = [(4*block_size-1, i) for i in range(block_size)]
def wrap(y):  # input is the square you're leaving. direction is implied.
        x = tuple(y)
        if x in left1: # to left 4, rev
            k = left1.index(x)
            return (left4[-1-k], np.array([0,1]))
        elif x in left3: # to top 4
            k = left3.index(x)
            return (top4[k], np.array([1,0]))
        elif x in left4: # to left 1, rev
            k = left4.index(x)
            return (left1[-k-1], np.array([0,1]))
        elif x in left6: # to top 1
            k = left6.index(x)
            return (top1[k], np.array([1,0]))

        elif x in right2: # to right 5, rev
            k = right2.index(x)
            return (right5[-1-k], np.array([0,-1]))
        elif x in right3: # to bottom 2
            k = right3.index(x)
            return (bottom2[k], np.array([-1,0]))
        elif x in right5: # to right 2, rev
            k = right5.index(x)
            return (right2[-1-k], np.array([0,-1]))
        elif x in right6: # to bottom 5
            k = right6.index(x)
            return (bottom5[k], np.array([-1,0]))

        elif x in top1: # to left 6
            k = top1.index(x)
            return (left6[k], np.array([0,1]))
        elif x in top2: # to bottom 6
            k = top2.index(x)
            return (bottom6[k], np.array([-1,0]))
        elif x in top4: # to left 3
            k = top4.index(x)
            return (left3[k], np.array([0,1]))

        elif x in bottom2: # to right 3
            k = bottom2.index(x)
            return (right3[k], np.array([0,-1]))
        elif x in bottom5: # to right 6
            k = bottom5.index(x)
            return (right6[k], np.array([0,-1]))
        elif x in bottom6: # to top 2
            k = bottom6.index(x)
            return (top2[k], np.array([1,0]))


##        draw()
        print('called wrap at', x, ', where grid is', grid[x[0], x[1]])



alpha_steps = [c.isalpha() for c in steps]
last_move = False
while not last_move:

##    print('At', x)
    
    if any(alpha_steps):
        i = alpha_steps.index(True)
        n = int(steps[:i])
        steps = steps[i:]
        alpha_steps = alpha_steps[i:]
        
        turn = steps[0]
        steps = steps[1:]
        _ = alpha_steps.pop(0)

##        print('  Go', n, 'then', turn)

    else:
        last_move = True
        n = int(steps)
        steps = []
##        print('  Go', n)

    
    for k in range(n):
        next_x = x + v
        next_v = np.copy(v)
##        print('    checking', next_x, end = '...')
        if next_x[0] < 0 or next_x[0] > H-1 or next_x[1] < 0 or next_x[1] > W-1 or grid[next_x[0], next_x[1]] == 0:
            next_x, next_v = wrap(x)
##            print('    wrapping from', x, 'to', next_x, arrow(next_v))
            
        if grid[next_x[0], next_x[1]] == 1:
            x = next_x
            v = next_v
            path[(x[0], x[1])] = arrow(v)
##            print(' moved')
        else:
##            print(' blocked')
            break

    if not last_move:
        if turn == 'R':
            v = np.dot(CW, v)
        else:
            v = np.dot(CCW, v)
##        print('  new direction:', arrow(v))
        path[(x[0], x[1])] = arrow(v)
        
##draw()



r = x[0] + 1
c = x[1] + 1
f = {'>':0, 'v':1, '<':2, '^':3}[path[(x[0], x[1])]]

print(r*1000 + 4*c + f)







