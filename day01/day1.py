with open('input.txt') as f :
    curr_sum = max_sum = 0
    top_3 = []
    for r in f:
        if len(r.strip()) == 0: # end of group
            max_sum = max(max_sum, curr_sum)
            if len(top_3) < 3:
                top_3.append(curr_sum)
            elif any([curr_sum > _ for _ in top_3]):
                # inefficient but meh
                top_3.append(curr_sum)
                top_3.sort() # sort the list
                top_3.pop(0) # the first item is smallest, remove
            curr_sum = 0
        else:
            curr_sum += int(r)

    print('Max: {}'.format(max_sum))
    print('Top 3: {}'.format(sum(top_3)))

