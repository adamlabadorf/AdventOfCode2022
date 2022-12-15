import json
from itertools import zip_longest
from functools import cmp_to_key
import logging


def is_int(x):
    return isinstance(x, int)

def int_cmp(a, b):
    r = 0
    if a > b:
        r = 1
    elif a < b:
        r = -1
    return r


def cmp(left, right):

    for elem1, elem2 in zip_longest(left, right):
        logging.debug('left, right: {} {}'.format(elem1, elem2))

        if elem1 is None: # ran out of left, in order
            logging.debug('ran out of left: {} {}'.format(elem1, elem2))
            return -1
        elif elem2 is None: # ran out of right, out of order
            logging.debug('ran out of right: {} {}'.format(elem1, elem2))
            return 1
        elif is_int(elem1) and is_int(elem2):
            logging.debug('integers: {} {}'.format(elem1, elem2))
            return elem1 - elem2 #int_cmp(elem1, elem2)
        else:
            if is_int(elem1): # left is int, right is list
                logging.debug('mixed type: {} {}'.format(elem1, elem2))
                elem1 = [elem1]

            elif is_int(elem2): # left is list, right is int
                logging.debug('mixed type: {} {}'.format(elem1, elem2))
                elem2 = [elem2]

            logging.debug('recurse: {} {}'.format(elem1, elem2))
            result = cmp(elem1, elem2)
            if result != 0:
                return result

    logging.debug('exhausted input')
    return 0

def flatten(l):
    r = []
    for li in l:
        if is_int(li):
            r.append(li)
        else:
            r.extend(flatten(li))

    return r

with open('input.txt') as f:

    logging.basicConfig(level=logging.INFO)

    codes = []

    logging.info('part 1')
    i = 1
    in_order = 0
    while True:
        logging.info(i)
        c1, c2 = json.loads(next(f)), json.loads(next(f))
        codes.append(c1)
        codes.append(c2)

        logging.debug('c1 {}'.format(c1))
        logging.debug('c2 {}'.format(c2))
        if cmp(c1, c2):
            logging.info('in order')
            in_order += i
        else:
            logging.info('not in order')
            pass

        # skip the empty line
        try:
            next(f)
        except StopIteration:
            break
        i += 1

    logging.info('in order: {}'.format(in_order))

    codes.extend([[[2]], [[6]]])

    #codes = [flatten(_) for _ in codes]
    #codes.sort()
    codes.sort(key=cmp_to_key(cmp))

    for code in codes:
        logging.info(code)

    divider1 = codes.index([[2]])+1
    divider2 = codes.index([[6]])+1

    logging.info('divider 1: %s', divider1)
    logging.info('divider 2: %s', divider2)
    logging.info('decoder key: %s', divider1*divider2)
