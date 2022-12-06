import string
letters = string.ascii_lowercase+string.ascii_uppercase
priority_map = dict(zip(letters, range(1, len(letters)+1)))

with open('input.txt') as f:
    tot_sum = 0
    for r in f:
        half = int(len(r)/2)
        r1, r2 = r[:half], r[half:]
        # naive, but meh
        in_common = [_ for _ in r1 if r2.find(_) != -1]

        tot_sum += priority_map[in_common[0]]

    print(tot_sum)
