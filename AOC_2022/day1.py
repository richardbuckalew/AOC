
test_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

with open('day1_input.txt', 'r') as f:
    data = f.readlines()

##data = test_data.splitlines()
    
packs = []
current_pack = []
while data:
    line = data.pop(0)
    if line == '' or line == '\n':
        packs.append(current_pack[:])
        current_pack = []
    else:
        current_pack.append(int(line))

cals = [sum(pack) for pack in packs]
print(sum(sorted(cals)[-3:]))
