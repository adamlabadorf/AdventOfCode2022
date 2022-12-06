play_map = dict(zip('XYZ', 'ABC'))
win_map = dict(zip('ABC', 'BCA'))
score_map = dict(zip('ABC', [1, 2, 3]))

def play(a, b):
    score = score_map[b]
    if a == b:
        score += 3
    elif b == win_map[a]:
        score += 6
    return score

with open('input.txt') as f:
    score = 0
    for r in f:
        a, b = r.strip().split(' ')
        b = play_map[b]
        score += play(a, b)

    print(score)
