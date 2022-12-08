from itertools import takewhile

def get_visible(row, from_pos=0):

    # to get the number of visible trees from any point in the row
    # rotate it so that from_pos is at index 0
    row = row[from_pos:]+row[:from_pos]

    left_max = right_max = -1
    visible = [False]*len(row)

    row = [int(_) for _ in row]
    for i in range(len(row)):
        t_l = row[i]
        if t_l > left_max:
            visible[i] = True
            left_max = t_l
        r_i = len(row)-i-1
        t_r = row[r_i]
        if t_r > right_max:
            visible[r_i] = True
            right_max = t_r
    return visible

def get_visible_shorter(row, from_pos=0):

    row = [int(_) for _ in row]
    pos_height = row[from_pos]

    left = row[:from_pos][::-1]
    shorter = list(takewhile(lambda x: x < pos_height, left))
    num_shorter = len(shorter)
    # edge case where the next tree is equal to pos_height
    if 0 < len(shorter) < len(left):
        num_shorter += left[len(shorter)] == pos_height

    right = row[from_pos+1:]
    shorter = list(takewhile(lambda x: x < pos_height, right))
    num_shorter *= len(shorter)
    # edge case where the next tree is equal to pos_height
    if 0 < len(shorter) < len(right):
        num_shorter += right[len(shorter)] == pos_height

    return num_shorter


with open('input.txt') as f:

    trees = f.read().strip().split('\n')
    # transposed trees are used in a couple places
    trees_transpose = [''.join(_) for _ in zip(*trees)]

    # get visibility along rows
    visible = [get_visible(_) for _ in trees]

    # transpose tree matrix to operate on rows
    visible_transpose = [get_visible(_) for _ in trees_transpose]

    # transpose it back because it makes unioning easier
    visible_transpose = [_ for _ in zip(*visible_transpose)]

    num_visible = 0
    for i in range(len(visible)):
        num_visible += sum(_1 or _2 for _1, _2 in zip(visible[i],visible_transpose[i]))

    print('num visible: {}'.format(num_visible))

    scenic_scores = []
    for row in trees:
        scenic_scores.append([get_visible_shorter(row, from_pos=i) for i in range(len(row))])

    scenic_scores_transpose = []
    for row in trees_transpose:
        scenic_scores_transpose.append([get_visible_shorter(row, from_pos=i) for i in range(len(row))])

    scenic_scores_transpose = [list(_) for _ in zip(*scenic_scores_transpose)]

    def rjust(x, n=4):
        return ''.join([str(_).rjust(n) for _ in x])

    i = 2
    print(rjust(range(len(scenic_scores[i]))))
    print(rjust(trees[i]))
    print(rjust(scenic_scores[i]))
    print(rjust(scenic_scores_transpose[i]))

    max_scenic_score = 0
    for scores1, scores2 in zip(scenic_scores, scenic_scores_transpose):
        sum_scores = [_[0]*_[1] for _ in zip(scores1, scores2)]
        max_scenic_score = max(max_scenic_score, max(sum_scores))

    print('max scenic score: {}'.format(max_scenic_score))
