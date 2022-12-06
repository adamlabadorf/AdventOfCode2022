import string
letters = string.ascii_lowercase+string.ascii_uppercase
priority_map = dict(zip(letters, range(1, len(letters)+1)))

def get_badge(group):
    in_common = set(group[0]).intersection(group[1]).intersection(group[2])
    return list(in_common)[0]

with open('input.txt') as f:
    tot_sum = 0
    group_sum = 0
    group = []
    for r in f:
        half = int(len(r)/2)
        r1, r2 = r[:half], r[half:]
        # naive, but meh
        in_common = [_ for _ in r1 if r2.find(_) != -1]

        tot_sum += priority_map[in_common[0]]

        if len(group) == 3:
            group_sum += priority_map[get_badge(group)]
            group = [r.strip()]
        else:
            group.append(r.strip())

    # last group badge
    group_sum += priority_map[get_badge(group)]

    print('Total priority: {}'.format(tot_sum))
    print('Group priority: {}'.format(group_sum))
