
test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

with open('day4_input.txt', 'r') as f:
    data = f.readlines()

##data = test_data.splitlines()
    
count = 0

for line in data:
    ranges = line.split(',')
    (a,b) = ranges[0].split('-')
    (c,d) = ranges[1].split('-')
    a = int(a); b = int(b); c = int(c); d = int(d)
    if (a <= c <= b) or (c <= b <= d) or (a <= d <= b) or (c <= a <= d):
        count += 1
        print((a,b), (c,d))

print(count)

