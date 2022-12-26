import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
from time import time

test_data = """1
2
-3
3
-2
0
4"""


##data = test_data.splitlines()

with open('day20_input.txt', 'r') as f:
    data = f.readlines()

K = 811589153
def parse_data(data):
    X = []
    for line in data:
        X.append(int(line) * K)
    return X


X = parse_data(data)
n = len(X)
print(X)
print('')

P = [i for i in range(n)]

for n_mix in range(10):

    for ip in range(n):

        ix = P.index(ip)
        x = X[ix]
        X.pop(ix)
        p = P.pop(ix)
        ix = (ix + x) % len(X)
        if ix == 0:
            X.append(x)
            P.append(p)
        else:
            X.insert(ix, x)
            P.insert(ix, p)

        ip += 1

    print(n_mix, X)


io = X.index(0)

io1k = (io + 1000) % n
io2k = (io + 2000) % n
io3k = (io + 3000) % n

print(X[io1k] + X[io2k] + X[io3k])






















