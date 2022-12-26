import numpy as np


test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


data = test_data.splitlines()


with open('day12_input.txt', 'r') as f:
    data = f.readlines()



M = len(data)
N = len(data[0])


H = np.zeros((M, N), int)

for m in range(M):
    for n in range(N):
        if data[m][n] == 'S':
            start = (m,n)
            H[m][n] = ord('a')
        elif data[m][n] == 'E':
            goal = (m,n)
            H[m][n] = ord('z')
        else:
            H[m,n] = ord(data[m][n])

print('height map:\n', H)


coords = [(i,j) for i in range(M) for j in range(N)]
G = np.zeros((M*N, M*N), bool)

for (ix, (a,b)) in enumerate(coords):
    for (jx, (c,d)) in enumerate(coords):
        if (a,b) == (c,d):
            continue
        if abs(a-c) + abs(b-d) > 1:
            continue
        if H[c,d] - H[a,b] <= 1:
            G[ix,jx] = True                 # FROM ix TO jx: G[ix,jx]

print('adjacency:\n', G)


best_length = 2*M*N

a_coords = [coord for coord in coords if H[coord[0], coord[1]] == ord('a')]

for a_coord in a_coords:

    print('from', a_coord)

    D = 2*(M*N) * np.ones((M*N), int) # max path length visits every square
    D[coords.index(a_coord)] = 0

    unvisited = np.ones(D.shape, bool)
    # unvisited[coords.index(start)] = False


    while any(unvisited):

        min_d = min(D[unvisited])
        for (i, d) in enumerate(D):
            if not unvisited[i]:
                continue
            if d == min_d:
                ix = i
                break

        nbrs = [(i, coord) for (i, coord) in enumerate(coords) if G[ix, i] and unvisited[i]]

        for (i, nbr) in nbrs:
            D[i] = min(D[i], D[ix] + 1)
        
        unvisited[ix] = False


        if ix == coords.index(goal):
            break

    p_length = D[coords.index(goal)]
    print(p_length)
    best_length = min(p_length, best_length)


# for (c, d) in zip(coords, D):
#     print(c, d)


print(best_length)





