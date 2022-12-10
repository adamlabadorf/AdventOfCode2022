from collections import defaultdict
from textwrap import wrap

with open('input.txt') as f:
    ops = defaultdict(list)
    register = defaultdict(int)
    cycle = 0
    register[0] = 1

    for r in f:
        if r.startswith('noop'):
            cycle += 1
            register[cycle] = register[cycle-1]+sum(ops[cycle-1])
        else:
            op, val = r.strip().split()
            val = int(val)
            cycle += 1
            register[cycle] = register[cycle-1]+sum(ops[cycle-1])
            cycle += 1
            register[cycle] = register[cycle-1]+sum(ops[cycle-1])
            ops[cycle].append(val)

# debug
#for i in range(220):
#    print('{}: X={} ops={} signal={}'.format(i, register[i], ops[i], (i+1)*register[i]))

signal_sum = 0
for i in range(20, 240, 40):
    signal_sum += register[i]*i
    print('{}*{} = {}'.format(i, register[i], register[i]*i))

print('signal sum: {}'.format(signal_sum))

screen = []
for i in range(40*6):
    r = register[i+1]
    if (i % 40) in (r-1, r, r+1):
        screen.append('#')
    else:
        screen.append('.')

print('\n'.join(wrap(''.join(screen), 40)))