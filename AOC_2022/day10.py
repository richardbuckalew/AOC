test_input = """noop
noop
noop
addx 5
addx 1
addx 4
addx 1
noop
addx 4
noop
addx 1
addx 4
addx 8
addx -7
addx 3
addx 1
noop
addx 4
addx 2
addx 5
addx -1
noop
addx -37
noop
noop
addx 3
addx 2
addx 13
addx 12
addx -15
addx -2
addx 2
addx -11
addx 18
addx 2
addx -15
addx 16
addx 5
addx 2
addx 5
noop
noop
noop
addx 3
addx -2
addx -38
noop
addx 3
addx 4
noop
noop
noop
noop
noop
addx 5
addx 5
noop
noop
addx 21
addx -17
addx 6
noop
noop
noop
noop
addx 5
noop
noop
noop
noop
noop
addx 3
addx 5
addx -38
noop
noop
addx 5
addx -2
addx 1
addx 7
noop
addx 22
addx -18
addx -11
addx 27
addx -13
addx 2
addx 5
addx -8
addx 9
addx 2
noop
addx 7
noop
addx 1
noop
addx -38
noop
addx 2
addx 5
addx -3
noop
addx 8
addx 11
addx -6
noop
addx 24
addx -31
addx 10
addx 2
addx 5
addx 3
noop
addx 2
addx -29
addx 21
addx 11
addx 5
addx -39
addx 4
addx -2
addx 2
addx 7
noop
addx -1
addx 2
noop
addx 4
noop
addx 1
addx 2
addx 5
addx 2
noop
noop
addx -6
addx 9
addx -18
addx 25
addx 3
noop
addx -17
noop"""


lines = test_input.splitlines()

X = 1
adding = False
V = 0
signal = []

crt = [[' '] * 40 for ix in range(6)]

cmd = 'noop'

cycle = 0
while lines or adding:
    
    cycle += 1
    if not adding:
        cmd = lines.pop(0)

##    print('Start cycle', cycle, ': begin executing', cmd)
    
    crt_line_number = (cycle // 40) % 6
    crt_pixel = cycle % 40 - 1

##    print('              CRT drawing in position', crt_pixel)

    
    if abs(crt_pixel - X) <= 1:
        crt[crt_line_number][crt_pixel] = '#'
    else:
        crt[crt_line_number][crt_pixel] = ' '

        
##    print(cycle, ':', cycle, '(op is', cmd, ')')
##    print('  Drawing at', crt_pixel, '(x =', X, ')')
##    print('  Current row:', ''.join(crt[crt_line_number]))
##    print('\n')
        
    
    if adding:
        X += V
        adding = False
    else:
        if cmd == 'noop':
            pass
        elif cmd[:4] == 'addx':
            V = int(cmd.split()[-1])
            adding = True


for crt_line in crt:
    print(''.join(crt_line))






