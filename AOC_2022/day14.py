import numpy as np
from ast import literal_eval
from collections import defaultdict

test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    


##data = test_data.splitlines()

with open('day14_input.txt', 'r') as f:
    data = f.readlines()




def parse_data(data):
    all_points = []
    all_paths = []
    max_y = 0
    for line in data:
        for (ix, x) in enumerate(line.split('->')):
            point = literal_eval('('+x+')')
            all_points.append(point)
            max_y = max(max_y, point[1])
            if ix > 0:
                all_paths.append([all_points[-2], all_points[-1]])
    return (all_paths, max_y + 2)



(all_paths, floor_y) = parse_data(data)


def build_grid(paths):
    grid = defaultdict(int)
    for (A, B) in paths:
        (a,b) = A
        (c,d) = B
        is_horizontal = (not a == c)
        is_vertical = (not b == d)
        if is_horizontal:
            for m in range(min(a,c), max(a,c)+1):
                grid[m,b] = 1
        elif is_vertical:
            for n in range(min(b,d), max(b,d)+1):
                grid[a, n] = 1
    return grid


chars = {0:' ', 1:'#', 2:'o'}
def draw_grid(grid):
    min_x = min([k[0] for (k,v) in grid.items() if v > 0])
    max_x = max([k[0] for (k,v) in grid.items() if v > 0])
    max_y = max([k[1] for (k,v) in grid.items() if v > 0])
    min_y = 0
    print('\n' + ' ' * (max_x - min_x + 4))
    for n in range(min_y, max_y+1):
        line = str(n) + ' '
        for m in range(min_x, max_x+1):
            line += chars[grid[(m,n)]]
        print(line)
##    print('')
    print('#' * (max_x - min_x+4))
##    print('\n')
            

grid = build_grid(all_paths)
draw_grid(grid)




source = (500, 0)
def falls(x, y):
    return [(x, y+1), (x-1, y+1), (x+1, y+1)]


def one_grain(grid, source):
    xy = source[:]
    while True:

##        temp_grid = grid.copy()
##        temp_grid[(xy[0], xy[1])] = 2
##        draw_grid(temp_grid)
            
##        print(' At', xy)
        moved = False
        for (tx, ty) in falls(*xy):
##            print('  checking', (tx, ty))
            if grid[(tx, ty)] == 0:
##                print('     moved to', (tx, ty))
                if ty == floor_y:
                    grid[(xy[0], xy[1])] = 2
                    return (grid, True)
                elif ty > floor_y:
##                    print('     abyss!')
                    return (grid, False)    # exit code: False means done
                xy = (tx, ty)
                moved = True
                break
        if not moved:
##            print('     at rest')
            grid[(xy[0], xy[1])] = 2
            return (grid, True)             # exit code: True means continue


##(grid, more_sand) = one_grain(grid, source)
more_sand = True
rested = 0
print('Dropping sand...', end = '')
while more_sand:
##    print('.', end = '')
    (grid, more_sand) = one_grain(grid, source)
    if grid[source] == 2:
        rested += 1
        break
    if more_sand:
        rested += 1


draw_grid(grid)
    

print(rested)
        














