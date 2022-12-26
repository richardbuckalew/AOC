import numpy as np

test_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def show_grid():
    xmin = min([v[0] for v in V] + [K[0] for K in rope])
    xmax = max([v[0] for v in V] + [K[0] for K in rope])
    ymin = min([v[1] for v in V] + [K[1] for K in rope])
    ymax = max([v[1] for v in V] + [K[1] for K in rope])

    for y in range(ymin-1, ymax+2):
        line = ''
        for x in range(xmin-1, xmax+2):
            if any([K[0] == x and K[1] == y for K in rope]):
                n = [K[0] == x and K[1] == y for K in rope].index(True)
                if n == 0:
                    line += 'H'
                elif n == 9:
                    line += 'T'
                else:
                    line += str(n)
            elif x == 0 and y == 0:
                line += 's'
            elif (x,y) in V:
                line += '#'
            else:
                line += '.'
        print(line)
    print('\n')



rope = [np.array([0,0]) for ix in range(10)]
V = [(0,0)]

step = {'R':np.array([1,0]), 'L':np.array([-1,0]), 'U':np.array([0,-1]), 'D':np.array([0,1])}


##C = test_input.splitlines()
with open('day9_input.txt', 'r') as f:
    C = f.readlines()

while C:
    cmd = C.pop(0)
    (d, n) = cmd.split()
    n = int(n)

    for ix in range(n):
        rope[0] += step[d]

##        show_grid()

        for ik in range(1,len(rope)):
            if max(abs(rope[ik-1] - rope[ik])) >= 2:
                rope[ik] += step['R']*np.sign(rope[ik-1][0] - rope[ik][0]) + step['D']*np.sign(rope[ik-1][1] - rope[ik][1])
        if not (tuple(rope[-1]) in V):
            V.append(tuple(rope[-1]))

##        show_grid()
##        print('------------')

##show_grid()
print(len(V))
        
        

    
