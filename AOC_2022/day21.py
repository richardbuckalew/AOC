import numpy as np
from ast import literal_eval
from collections import defaultdict
from random import randint
import math
from time import time

test_data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


##data = test_data.splitlines()

with open('day21_input.txt', 'r') as f:
    data = f.readlines()


class Monkey:
    def __init__(self, D, name, is_const, c, op, P, L, R):
        self.D = D
        self.name = name
        self.is_const = is_const
        self.c = c
        self.op = op
        self.P = P
        self.L = L
        self.R = R

    def value(self):
        if self.is_const:
            v = self.c
        else:
            if self.op == '+':
                v = D[self.L].value() + D[self.R].value()
            elif self.op == '-':
                v = D[self.L].value() - D[self.R].value()
            elif self.op == '*':
                v = D[self.L].value() * D[self.R].value()
            elif self.op == '/':
                v = D[self.L].value() // D[self.R].value()
        return v

    def L_inverse(self, rval, target):
        if self.is_const:
            raise(ValueError('Cannot invert a constant'))
        if self.op == '+':
            return target - rval
        elif self.op == '-':
            return target + rval
        elif self.op == '*':
            return target // rval
        elif self.op == '/':
            return target * rval

    def R_inverse(self, lval, target):
        if self.op == '+':
            return target - lval
        elif self.op == '-':
            return lval - target
        elif self.op == '*':
            return target // lval
        elif self.op == '/':
            return lval // target

    """Partially evaluates self.value(); getting the value from the non-human side and telling the
        human side what value it needs to return, in order for self to return target."""
    def balance(self, target):
        if self.name == 'humn':
            return target
        if self.L in H:     
            v = D[self.R].value()
            L_target = self.L_inverse(v, target)
##            print(self, ';    target', target, 'and', self.R, '=', v, 'so I need', self.L, '=', L_target)
            return D[self.L].balance(L_target)
        elif self.R in H:
            v = D[self.L].value()
            R_target = self.R_inverse(v, target)
            return D[self.R].balance(R_target)

    def __str__(self):
        if self.is_const:
            return self.name + ': ' + str(self.c)
        else:
            return self.name + ': ' + self.L + ' ' + self.op + ' ' + self.R
        

        

def parse_data(data):
    M = []
    D = dict()
    for line in data:
        words = line.split()
        if len(words) == 2:
            name = words[0][:-1]
            is_const = True
            c = int(words[1])
            L = 0
            R = 0
            op = ''
        elif len(words) == 4:
            name = words[0][:-1]
            is_const = False
            c = 0
            L = words[1]
            R = words[3]
            op = words[2]
        M.append(Monkey(D, name, is_const, c, op, 'P', L, R))
        D[name] = M[-1]
    for m in M:
##        print(m)
        if not m.is_const:
            D[m.L].P = D[m.R].P = m.name
    n = 'humn'
    H = [n]                     # the path that ends in 'humn'
    while not n == 'root':
        n = D[n].P
        H.append(n)
    return (M, D, H)

(M, D, H) = parse_data(data)
##print(H)

r = D['root']
##print(r)

if r.L in H:
    v = D[r.R].value()
##    print(v)
    target = D[r.L].balance(v)
else:
    v = D[r.L].value()
##    print(v)
    target = D[r.R].balance(v)

print(target)











