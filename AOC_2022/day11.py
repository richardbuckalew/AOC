test_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

from math import prod

class Monkey:
    def __init__(self, items, op, test):
        self.items = items
        self.op = op
        self.test = test
    def __str__(self):
        return 'M: ' + str(self.items)




def parse_data(data):
    def make_test(n, t, f):
        return lambda x: t if not x % n else f
    K = 1
    M = []
    while data:
        mdata = data[:6]
        for (nline, line) in enumerate(mdata):
            if line[:6] == 'Monkey':
                n = int(line.split()[1][:-1])
            elif line[:8] == '  Starti':
                X = line.split(':')
                X = X[1].split(',')
                items = [int(x) for x in X]
            elif line[:4] == '  Op':
                X = line.split(':')
                rhs = X[-1].split('=')[-1]
                print('lambda old:' + rhs)
                op = eval('lambda old:' + rhs)
            elif line[:4] == '  Te':
                n = int(line.split()[-1])
                true_target = int(mdata[nline+1].split()[-1])
                false_target = int(mdata[nline+2].split()[-1])
                K *= n
        M.append(Monkey(items, op, make_test(n, true_target, false_target)))
        try:
            data = data[7:]
        except:
            break        
    return (M, K)

                
    


##(M, K) = parse_data(test_data.splitlines())
with open('day11_input.txt', 'r') as f:
    (M, K) = parse_data(f.readlines())


n_monkeys = len(M)
counts = [0] * n_monkeys

for n_round in range(10000):
##    print('Round #', n_round+1)
    for (n_monkey, monkey) in enumerate(M):
##        print('  Monkey #', n_monkey)
        while monkey.items:
            counts[n_monkey] += 1
            x = monkey.items.pop(0)
            x = monkey.op(x)
##            x = x // 3
            x = x % K
            k = monkey.test(x)
            M[k].items.append(x)

            
print(counts)

Y = prod(sorted(counts)[-2:])
print(Y)











