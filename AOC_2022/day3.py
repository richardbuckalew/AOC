test_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

with open('day3_input.txt', 'r') as f:
    validate_input = f.readlines()

##validate_input = test_input.splitlines()


def priority(c):
    if c.islower():
        return ord(c) - 96
    else:
        return ord(c) - 38


common = []
lines = validate_input

badges = []

while lines:
    sacks = lines[:3]
    try:
        lines = lines[3:]
    except:
        break
    for c in sacks[0][:-1]:
        if c in sacks[1] and c in sacks[2]:
            badges.append(c)
            break
    


##for line in lines:
##    n = len(line)
##    C1 = line[:n//2]
##    C2 = line[n//2:]
##
##    for c in C1:
##        if c in C2:
##            common.append(c)
##            break

print(badges)
print([priority(c) for c in badges])
print(sum([priority(c) for c in badges]))
