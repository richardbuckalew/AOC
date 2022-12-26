import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint

test_data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

    


##data = test_data.splitlines()

with open('day15_input.txt', 'r') as f:
    data = f.readlines()




def parse_data(data):
    S = []  # sensors
    B = []  # beacons
    D = []  # distances
    for line in data:
        (s, b) = line.split(':')
        (x, y) = s.split(',')
        x = int(x.split()[-1].split('=')[-1])
        y = int(y.split('=')[-1])
        S.append((x, y))
        (x, y) = b.split(',')
        x = int(x.split()[-1].split('=')[-1])
        y = int(y.split('=')[-1])
        B.append((x, y))
        D.append(md(S[-1], B[-1]))
    return (S, B, D)


def md(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def objective(E):
##    print(D, E)
    x = 0
    for (d, e) in zip(D, E):
        x += max(0, d-e+1)
    return x


(S, B, D) = parse_data(data)


def nbrs(x, y):
    return [(x-1, y), (x-1, y-1), (x-1, y+1),
            (x+1, y), (x+1, y-1), (x+1, y+1),
            (x, y-1), (x, y+1)]



m = 0
n = 4000000
##n = 20
found = False
for (s, d) in zip(S, D):

    print('Sensor:', s, 'd:', d)
    X = list(range(s[0]-d-1, s[0]+d+1))
    Y = [s[1] + ((s[0]-x)-d-1) for x in X]
    Y.extend([s[1] - ((s[0]-x)-d-1) for x in X]) 
    X.extend(list(range(s[0]+d+1, s[0]-d-2, -1)))
    
    for (x,y) in zip(X, Y):

##        print(' ', (x,y))

        if x < m or y < m or x > n or y > n:
            continue

        E = [md((x, y), s) for s in S]
        o = objective(E)

        if o == 0:
            found = True
            print((x, y), ':', x*4000000+y)
            break
    if found:
        break
        





























