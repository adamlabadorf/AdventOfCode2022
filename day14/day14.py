from collections import defaultdict, namedtuple
from itertools import product
import math

Pos = namedtuple('Pos', ('x', 'y'))
Pos.down = lambda self: Pos(self.x, self.y+1)
Pos.down_left = lambda self: Pos(self.x-1, self.y+1)
Pos.down_right = lambda self: Pos(self.x+1, self.y+1)
Pos.up = lambda self: Pos(self.x, self.y-1)

class CaveSlice(object):
    def __init__(self):
        self.positions = defaultdict(lambda: '.')
        self.num_sand = 0

    def read_paths(self, fn):

        with open(fn) as f:
            paths = []
            xmin, xmax = 1e10, 0
            # ymin is always zero
            ymin, ymax = 0, 0
            for r in f:
                segs = r.split(' -> ')
                coords = [Pos(*map(int, _.split(','))) for _ in segs]

                for c1, c2 in zip(coords, coords[1:]):
                    minx, miny = min(c1.x, c2.x), min(c1.y, c2.y)
                    maxx, maxy = max(c1.x, c2.x), max(c1.y, c2.y)
                    for p in product(range(minx, maxx+1), range(miny, maxy+1)):
                        self[Pos(*p)] = '#'

                xmin = min(xmin, min([_[0] for _ in coords]))
                xmax = max(xmax, max([_[0] for _ in coords]))

                #ymin = min(ymin, min([_[1] for _ in coords]))
                ymax = max(ymax, max([_[1] for _ in coords]))

            self.xmin, self.xmax, self.xlen = xmin, xmax, xmax-xmin
            self.ymin, self.ymax, self.ylen = ymin, ymax, ymax

    def add_floor(self, width=None):
        if not width:
            width = self.ymax+3
        self.xmin -= width
        self.xmax += width
        for i in range(self.xmin, self.xmax):
            self[Pos(i, self.ymax+2)] = '#'

    def simulate(self, origin=Pos(500, 0)):
        curr_pos = origin
        while True:
            dirs = [curr_pos.down(), curr_pos.down_left(), curr_pos.down_right()]
            for next_pos in dirs:
                if self[next_pos] == '.':
                    curr_pos = next_pos
                    break

            # if we didn't move, set sand symbol and restart
            if curr_pos != next_pos:
                self.num_sand += 1
                self[curr_pos] = 'o'
                # if sand didn't move off origin, stop
                if curr_pos == origin:
                    break
                curr_pos = origin

            # if we fall off the end, stop
            if curr_pos.y >= self.ymax+3:
                break

    def get_top(self):
        sand_positions = [p for p,c in self.positions.items() if c == 'o']
        return min(sand_positions, key=lambda p: (abs(p.x-500), p.y))

    def __getitem__(self, item):
        return self.positions[item]

    def __setitem__(self, key, value):
        self.positions[key] = value

    def __str__(self):
        out = []
        yaxis_pad = math.ceil(math.log(self.ymax+2, 10))
        for j in range(self.ymin, self.ymax+3):
            out.append([str(j).ljust(yaxis_pad), ' '])
            for i in range(self.xmin-3, self.xmax+3):
                out[-1].append(self.positions[Pos(i, j)])
        return '\n'.join([''.join(_) for _ in out])

cave = CaveSlice()
cave.read_paths('input.txt')
cave.simulate()
wo_floor = cave.num_sand

cave.add_floor()
cave.simulate()
print('wo floor:',wo_floor)
print('w floor:', cave.num_sand)
