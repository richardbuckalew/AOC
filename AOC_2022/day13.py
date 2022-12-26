from functools import cmp_to_key

test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    


##data = test_data.splitlines()

with open('day13_input.txt', 'r') as f:
    data = f.readlines()



def compare(A, B): # returns 0 if unsure, 1 if bad, 2 if good
##    print(' ', A, 'vs', B)
    if type(A) == type(B) == list:
##        print('    (lists)')
        for i in range(min(len(A), len(B))):
            a = A[i]
            b = B[i]
            c = compare(a,b)
            if c:
                return c
        if len(A) > len(B):
            return 1
        elif len(B) > len(A):
            return 2
        else:
            return 0
    elif type(A) == type(B) == int:
##        print('    (ints)')
        if A < B:
##            print('    A < B')
            return 2
        elif A > B:
##            print('    A > B')
            return 1
        else:
##            print('    A == B')
            return 0
    else:
##        print('    (mixed)')
        if type(A) == int:
            return compare([A], B[:])
        else:
            return compare(A[:], [B])



def le(A, B):
    c = compare(A[:], B[:])
    return {0:0, 1:1, 2:-1}[c]
    




all_packets = []
correct = []
n_pair = 0
while data:
    n_pair += 1
    try:
        lines = data[:3]
        data = data[3:]
    except:
        lines = data[:2]
        data = data[2:]

    all_packets.extend([eval(lines[0]), eval(lines[1])])

##    print(n_pair, ':', lines[0], 'vs', lines[1])
    result = compare(eval(lines[0])[:], eval(lines[1])[:])
##    print(int(result))
    if result == 2:
        correct.append(n_pair)
##    print('\n')

##print(correct, ':', sum(correct))

        
all_packets.extend([ [[2]], [[6]] ])

print(all_packets)

all_packets.sort(key = cmp_to_key(le))

print((all_packets.index([[2]])+1) * (all_packets.index([[6]])+1))












