with open('input.txt') as f :
    curr_sum = max_sum = 0
    for r in f:
        if len(r.strip()) == 0: # end of group
            max_sum = max(max_sum, curr_sum)
            curr_sum = 0
        else:
            curr_sum += int(r)

    print(max_sum)

