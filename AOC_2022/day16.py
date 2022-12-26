import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
from math import nan

test_data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


##['JJ', 'BB', 'CC']
##['DD', 'HH', 'EE']
##data = test_data.splitlines()

with open('day16_input.txt', 'r') as f:
    data = f.readlines()


T = 26


def parse_data(data):

    V = []
    flow = {}
    nbrs = {}
    
    for line in data:
        (v, t) = line.split(';')
        words = v.split()
        valve = words[1]
        nbrs[valve] = []
        rate = int(words[-1].split('=')[-1])
        parts = t.split(', ')
        for part in parts:
            nbrs[valve].append(part.strip()[-2:])
        V.append(valve)
        flow[valve] = rate

    
        
    B = np.zeros((len(V), len(V)), int)     # full adjacency matrix
    for (n, v) in enumerate(V):
        for w in nbrs[v]:
            B[n,V.index(w)] = 1

    BB = [np.linalg.matrix_power(B, k) for k in range(1, len(V))]

    nonzero = [v for v in V if flow[v] > 0]
    A = np.zeros((len(nonzero), len(nonzero)))

    A = np.zeros((len(V), len(V)), int)
    for (m, v) in enumerate(V):
        for (n, w) in enumerate(V):
            for d in range(len(V)):
                if BB[d][m,n] or BB[d][n,m]:
                    A[m,n] = d+1
                    A[n,m] = d+1
                    break


    return (V, nonzero, flow, A)


(V, N, F, A) = parse_data(data)
full_rate = sum(F.values())
##print(N, '\n', F, '\n', A)

def solve(v1, v2, path1, path2, value, t1, t2):
##    print(path, value, t)
    if t1 >= T and t2 >= T:
        return value

    if t1 <= t2:
        v = v1
        t = t1
    else:
        v = v2
        t = t2
    

    options = [n for n in N if n not in path1+path2 and A[V.index(n), V.index(v)] < T-t]
    if not options:
##        print(path1, path2, value)
        return value
    opt_values = []
    for n in options:
        d = A[V.index(n),V.index(v)]
        value_add = F[n] * (T - (t + 1 + d))

        if t1 <= t2:        
            opt_values.append(solve(n, v2, path1 + [n], path2, value+value_add, t1 + 1 + d, t2))
        else:
            opt_values.append(solve(v1, n, path1, path2 + [n], value+value_add, t1, t2 + 1 + d))

    return max(opt_values)

x = solve('AA', 'AA', [], [], 0, 0, 0)
print(x)






























