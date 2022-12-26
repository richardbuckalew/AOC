import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
import time

test_data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


# data = test_data.splitlines()

with open('day25_input.txt', 'r') as f:
   data = f.readlines()


def sym(c):
    if c.isnumeric():
        return int(c)
    else:
        return {'-':-1, '=':-2}[c]

def dec(snafu, b=5):
    d = 0
    n = len(snafu)
    for (k, c) in enumerate(snafu):
        d += sym(c) * b**(n-k-1)
    return d

C = '012=-'
def snafu(dec, b=5):
    s = ''
    for k in range(math.ceil(math.log(dec, b))+1, -1, -1):
        r = dec
        for i in range(k):
            r = (r + 2) // b
        s += C[r%b]
    return s.lstrip('0')

def test():
    for d in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 2022, 12345, 314159265]:
        s = snafu(d)
        testd = str(dec(s))
        print(str(d).ljust(10, ' '), ':', s.rjust(15, ' '), ':', testd.ljust(10, ' '))


def process(data):
    D = []
    for line in data:
        d = dec(line.strip())
        D.append(d)
    print(sum(D), ':', snafu(sum(D)))

process(data)
        





