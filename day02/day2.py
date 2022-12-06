play_map = dict(zip('XYZ', 'ABC'))
win_map = dict(zip('ABC', 'BCA'))
lose_map = dict(zip('ABC', 'CAB'))
score_map = dict(zip('ABC', [1, 2, 3]))

def play(a, b):
    score = score_map[b]
    if a == b:
        score += 3
    elif b == win_map[a]:
        score += 6
    return score

with open('input.txt') as f:
    part1_score = part2_score = 0
    for r in f:
        a, b = r.strip().split(' ')
        part1_score += play(a, play_map[b])

        if b == 'X':
            b = lose_map[a]
        elif b == 'Y':
            b = a
        else:
            b = win_map[a]
        part2_score += play(a, b)

    print('Part 1: {}'.format(part1_score))
    print('Part 2: {}'.format(part2_score))
