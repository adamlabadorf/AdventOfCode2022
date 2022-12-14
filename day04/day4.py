with open('input.txt') as f:
    containing = 0
    overlapping = 0
    for r in f:
        r1, r2 = [list(map(int,_.split('-'))) for _ in r.strip().split(',')]
        # naive but meh
        if (r1[0] <= r2[0] and r1[1] >= r2[1] or
            r2[0] <= r1[0] and r2[1] >= r1[1]):
            containing += 1
        # inefficient but meh
        overlap = set(range(r1[0], r1[1]+1)).intersection(range(r2[0], r2[1]+1))
        overlapping += len(overlap) > 0
    print('Containing: {}'.format(containing))
    print('Overlapping: {}'.format(overlapping))
