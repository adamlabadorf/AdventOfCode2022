with open('day5.txt', 'r') as f:
    stacks = []
    for r in f:
        if len(r.strip()) == 0:
            break
        # remove [ and ] because we don't need them
        r = r.replace('[','').replace(']','').replace('  ',' ').strip()
        stacks.append(r)

    # remove the stack number line because we don't need them
    stacks.pop()

    # transpose stacks strings to make parsing easier
    # pure python becuz shrug
    max_len = max([len(_) for _ in stacks])
    stacks = zip(*[_.ljust(max_len)[::2] for _ in stacks if _[0] != ' '][::-1])

    # get rid of empty crates and convert to lists
    stacks = [list([_ for _ in stack if _ != ' ']) for stack in stacks]

    # perform ops
    for r in f:
        amt, frm, to = [int(_) for _ in r.split()[1::2]]
        stacks[to-1].extend(stacks[frm-1][-amt:][::-1])
        stacks[frm-1] = stacks[frm-1][:-amt]

    for i, stack in enumerate(stacks):
        print('{}: {}'.format(i+1, stack[-1]))


