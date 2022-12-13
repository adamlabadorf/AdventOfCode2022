from collections import namedtuple
import networkx as nx
from itertools import product
import numpy as np
import matplotlib.pyplot as plt

Pos = namedtuple('Pos',('x','y'))

with open('input.txt') as f:

    topo = f.read().strip().split('\n')
    xlen, ylen = len(topo[0]), len(topo)

    # find S and E
    start = None
    end = None
    for y in range(len(topo)):
        for x in range(len(topo[0])):
            if topo[y][x] == 'S':
                start = Pos(x, y)
                topo[y] = topo[y].replace('S', chr(ord('a')))
            if topo[y][x] == 'E':
                end = Pos(x, y)
                topo[y] = topo[y].replace('E', chr(ord('z')))

    nodes = [Pos(*_) for _ in product(range(xlen), range(ylen))]
    g = nx.DiGraph()
    g.add_nodes_from(nodes)

    for pos in g.nodes:

        next_positions = [
            Pos(pos.x-1, pos.y), # left
            Pos(pos.x, pos.y-1), # up
            Pos(pos.x+1, pos.y), # right
            Pos(pos.x, pos.y+1) # down
        ]

        viable_steps = []
        for next_pos in next_positions:
            # out of bounds
            if any([next_pos.y < 0, next_pos.x < 0, next_pos.y >= ylen, next_pos.x >= xlen]) :
                #print('out of bounds: {}'.format(next_pos))
                continue
            # can't go up more than one level
            if ord(topo[next_pos.y][next_pos.x]) - ord(topo[pos.y][pos.x]) > 1:
                #print('too steep: {} >> {}'.format(topo[next_pos.y][next_pos.x], topo[pos.y][pos.x]))
                continue
            g.add_edge(pos, next_pos)

    path = nx.shortest_path(g, start, end, method='dijkstra')

    path_map = [['.']*xlen for _ in range(ylen)]


    for p1, p2 in zip(path, path[1:]):
        c = '.'
        if p1.x < p2.x:
            c = '>'
        elif p1.x > p2.x:
            c = '<'
        elif p1.y < p2.y:
            c = 'v'
        elif p1.y > p2.y:
            c = '^'
        else:
            print(p1, p2)

        path_map[p1.y][p1.x] = c

    for t, p in zip(topo, path_map):
        print(''.join(p))
        print(''.join(t))

    print(len(path)-1)

    topo_ord = np.array([[ord(_) for _ in topo[i]] for i in range(len(topo))])
    for step in path:
        topo_ord[step.y, step.x] = ord('z')+1
    plt.pcolormesh(np.flip(topo_ord, 0))
    plt.show()

    # the reverse edge graph will let us search from E to the nearest a
    rev_g = g.reverse(copy=True)

    first_a = None
    for n1, n2 in nx.bfs_edges(rev_g, end):
        if topo[n2.y][n2.x] == 'a':
            first_a = n2
            break

    path = nx.shortest_path(rev_g, end, first_a, method='dijkstra')

    topo_ord = np.array([[ord(_) for _ in topo[i]] for i in range(len(topo))])
    for step in path:
        topo_ord[step.y, step.x] = ord('z')+1
    plt.pcolormesh(np.flip(topo_ord, 0))
    plt.show()

    print(len(path)-1)
