
def move(x):
    ''' returns +1 or -1 based on the move of the argument'''
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

with open('input.txt') as f:

    tail_positions = set()

    num_knots = 10
    knots = [(0, 0)]*num_knots
    prev_knots = [(0, 0)]*num_knots

    tail_positions.add(knots[-1])

    for r in f:
        direction, steps = r.strip().split()
        steps = int(steps)

        for i in range(steps):

            head = knots[0]

            # update the head knot
            if direction == 'U':
                head = (head[0], head[1]+1)
            elif direction == 'R':
                head = (head[0]+1, head[1])
            elif direction == 'D':
                head = (head[0], head[1]-1)
            else:
                head = (head[0]-1, head[1])

            knots[0] = head

            # evaluate and update every knot in the rope
            for knot_i in range(len(knots)-1):

                knot_1 = knots[knot_i]
                knot_2 = knots[knot_i+1]

                # determine if the next knot needs to move
                # next knot only moves if the previous knot is 2 steps away in any direction
                if (abs(knot_1[0]-knot_2[0]) > 1 or abs(knot_1[1]-knot_2[1]) > 1):

                    # this is how ropes actually work, but not what the problem wants
                    #knots[knot_i+1] = prev_knots[knot_i]

                    new_knot_pos = list(knot_2)

                    # horizontal move
                    horiz = knot_1[0]-knot_2[0]

                    # vertical move
                    vert = knot_1[1]-knot_2[1]

                    # we move either +1, -1, or 0 in either direction
                    # depending on the move of the delta between knot 1 and knot 2
                    new_knot_pos[0] += move(horiz)
                    new_knot_pos[1] += move(vert)

                    knots[knot_i+1] = tuple(new_knot_pos)

            prev_knots = knots.copy()
            tail_positions.add(knots[-1])

print(len(tail_positions))