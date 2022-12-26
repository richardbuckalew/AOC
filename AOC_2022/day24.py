import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
import time

test_data = """#.######
#>>.<^<#
#.<..<<#
#>v.><># 
#<^v^^>#
######.#"""


# data = test_data.splitlines()

with open('day24_input.txt', 'r') as f:
   data = f.readlines()





def parse_data(data):
    H = len(data)
    W = max([len(line) for line in data]) - 1
    # W = 122

    G = np.zeros((H, W))
    U = np.zeros((H-2,W-2))     # holds all upward moving blizzards. Can roll these
    D = np.zeros_like(U)
    L = np.zeros_like(U)
    R = np.zeros_like(U)

    for (i, line) in enumerate(data):
        for (j, c) in enumerate(line):
            if c == '#':
                G[i,j] = 2
            elif c == '.':
                if i == 0:
                    start = (i,j)
                elif i == H-1:
                    goal = (i,j)
                G[i,j] = 0
            elif c == '^':
                U[i-1,j-1] = 1
            elif c == '<':
                L[i-1,j-1] = 1
            elif c == '>':
                R[i-1,j-1] = 1
            elif c == 'v':
                D[i-1,j-1] = 1
    
    return (H, W, G, U, D, L, R, start, goal)
        

(H, W, G, U, D, L, R, start, goal) = parse_data(data)

def draw(H, W, G, U, D, L, R, start, goal, E):
    BB = U + D + L + R
    for i in range(H):
        s = ''
        for j in range(W):
            if E == (i,j):
                s += 'E'
            elif start == (i,j):
                s += 'S'
            elif goal == (i,j):
                s += 'G'
            else:
                if i == 0 or i == H-1 or j == 0 or j == W-1:
                    s += '#'
                else:        
                    k = BB[i-1,j-1]
                    if k == 0:
                        s += ' '
                    else:
                        s += '"'
        print(s)
    print('\n')


class Future:
    def __init__(self, H, W, U, D, L, R):
        self.F = [(U.copy(), D.copy(), L.copy(), R.copy())]        
        self.n = (H-2) * (W-2)
        for t in range(self.n):            
            (U, D, L, R) = self.F[-1]
            self.F.append((np.roll(U, -1, axis=0), np.roll(D, 1, axis=0), np.roll(L, -1, axis=1), np.roll(R, 1, axis=1)))

        for i in range(4):
            assert(np.all(np.equal(self.F[0][i], self.F[-1][i])))

    def __call__(self, t):
        return self.F[t % self.n]


F = Future(H, W, U, D, L, R)

draw(H, W, G, *F(0), start, goal, start)


def cross(x):
    return ((x[0], x[1]+1, x[2]+1), (x[0], x[1]-1, x[2]+1), (x[0]+1, x[1], x[2]+1), (x[0]-1, x[1], x[2]+1), (x[0], x[1], x[2]+1))



def solve():

    B = np.zeros((H-2, W-2, F.n), int)                      # all blizzards are static when you see in 3-d
    for t in range(F.n):
        B[:,:,t] = sum(F(t))

    Q = []
    D = np.ones_like(B) * 999999
    V = np.zeros_like(B)
    P = dict()
    (si, sj) = (0, start[1]-1)                       # start is outside the B grid, but we can only enter from one direction.
    (gi, gj) = (H-3, goal[1]-1)   
    ### CONSIDER VECTORIZING:                      
    for t in range(F.n-1):                                    # set initial Ds
        if not B[si, sj, t]:                                # if there is no blizzard next to start at time t
            D[si, sj, t] = t+1                              # then we can enter the grid there.
            Q.append((si, sj, t+1))                         # queue it up to initialize the search
            P[(si, sj, t+1)] = None
        V[gi,gj,t] = 1                                      # mark all goal cells as visited so they don't get enqueued

    while Q:
        (i, j, t) = Q.pop()
        V[i,j,t] = 1
        for (ni,nj,nt) in cross((i,j,t)):
            if ni < 0 or ni > H-3 or nj < 0 or nj > W - 3 or nt < 1 or nt >= F.n:
                continue
            if B[ni,nj,nt]:
                continue
            # if (ni,nj) == (gi,gj):      # goal
            #     P[(ni,nj,nt)] = (i,j,t)
            #     D[(ni,nj,nt)] = D[(i,j,t)] + 1
            #     return (nt, P, (gi, gj))
            d = D[i,j,t]+1
            if d < D[ni,nj,nt]:
                D[ni,nj,nt] = d
                P[ni,nj,nt] = (i,j,t)

            if (not V[ni,nj,nt]):
                Q.append((ni,nj,nt))

    tbest = np.argmin(D[gi,gj,:])
    return (tbest, P, (gi,gj), B, D)

def gensolve(forward, t0):

    B = np.zeros((H-2, W-2, F.n), int)                      # all blizzards are static when you see in 3-d
    for t in range(t0, t0 + F.n):
        B[:,:,t-t0] = sum(F(t))

    Q = []
    D = np.ones_like(B) * 999999
    V = np.zeros_like(B)
    P = dict()
    if forward:
        (si, sj) = (0, start[1]-1)                       # start is outside the B grid, but we can only enter from one direction.
        (gi, gj) = (H-3, goal[1]-1)  
    else:
        (si, sj) = (H-3, goal[1]-1)
        (gi, gj) = (0, start[1] - 1) 
    ### CONSIDER VECTORIZING:                      
    for t in range(F.n-1):                                    # set initial Ds
        if not B[si, sj, t]:                                # if there is no blizzard next to start at time t
            D[si, sj, t] = t+1                              # then we can enter the grid there.
            Q.append((si, sj, t+1))                         # queue it up to initialize the search
            P[(si, sj, t+1)] = None
        V[gi,gj,t] = 1                                      # mark all goal cells as visited so they don't get enqueued

    while Q:
        (i, j, t) = Q.pop()
        V[i,j,t] = 1
        for (ni,nj,nt) in cross((i,j,t)):
            if ni < 0 or ni > H-3 or nj < 0 or nj > W - 3 or nt < 1 or nt >= F.n:
                continue
            if B[ni,nj,nt]:
                continue
            # if (ni,nj) == (gi,gj):      # goal
            #     P[(ni,nj,nt)] = (i,j,t)
            #     D[(ni,nj,nt)] = D[(i,j,t)] + 1
            #     return (nt, P, (gi, gj))
            d = D[i,j,t]+1
            if d < D[ni,nj,nt]:
                D[ni,nj,nt] = d
                P[ni,nj,nt] = (i,j,t)

            if (not V[ni,nj,nt]):
                Q.append((ni,nj,nt))

    tbest = np.argmin(D[gi,gj,:])
    return (tbest, P, (gi,gj), B, D)

# soln = solve()
# soln = gensolve(True, 18)

s1 = gensolve(True, 0)
t1 = s1[0] + 1
print(t1)
s2 = gensolve(False, s1[0]+1)
t2 = s2[0] + 1
print(t2)
s3 = gensolve(True, s1[0]+1+s2[0]+1)
t3 = s3[0] + 1
print(t3)
print(t1+t2+t3)


# if soln:
#     (t, P, g, B, D) = soln
#     print('\nFound a path in', t+1, 'steps')
#     time.sleep(1)
#     path = [(g[0], g[1], t)]
#     while P[path[0]]:
#         path.insert(0, (P[path[0]]))

        
#     for (n, p) in enumerate(path[1:]):
#         p_old = path[n]
#         d = abs(p[0] - p_old[0]) + abs(p[1] - p_old[1])
#         b = B[p[0], p[1], p[2]]
#         assert(d <= 1)
#         assert(b == 0)

    
#     twait = path[0][2]
#     for wt in range(twait-1, -1, -1):
#         path.insert(0, (-1, 0, wt))
#     path.append((H-2, W-3, t+1))



#     for (i, j, tt) in path:
#         print('  t:', tt)
#         draw(H, W, G, *F(tt), start, goal, (i+1, j+1))
#         # print('x:', (i+1,j+1), 'B:', B[i,j,tt])
#         time.sleep(0.1)








