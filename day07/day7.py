class File(object):
    def __init__(self, name, size, parent):
        self.name = name
        self.size = size
        self.parent = parent
        self.type = 'file'

    def abspath(self):
        return ''.join([self.parent.abspath(),'{} (size={})'.format(self.name, self.size)])

    def __repr__(self):
        return 'File({}, {}, {})'.format(repr(self.name), repr(self.size), repr(self.parent))


class Dir(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.contents = {}
        self.type = 'dir'

    def mkdir(self, name):
        self.contents[name] = Dir(name, self)

    def touch(self, name, size):
        self.contents[name] = File(name, size, self)

    @property
    def size(self):
        tot_size = 0
        for entry_name, entry in self.contents.items():
            tot_size += entry.size
        return tot_size

    def abspath(self):
        out = ['{}/'.format(self.name)]
        parent = self.parent
        while parent is not None:
            out.insert(0, '{}/'.format(parent.name))
            parent = parent.parent
        return ''.join(out)

    def __iter__(self):
        return iter(self.contents.items())

    def __getitem__(self, item):
        return self.contents[item]

    def __repr__(self):
        return 'Dir({}, {})'.format(repr(self.name), repr(self.parent))

    def __str__(self):
        return ''.join([self.abspath(),'(size={})'.format(self.size)])


def walk(d, func, res):
    #print(''.join([d.abspath(), '(size={})'.format(d.size)]))
    for name, entry in d:
        if entry.type == 'dir':
            if func(entry.size):
                res.append(entry)
            res = walk(entry, func, res)
        #else:
        #    print(entry.abspath())

    return res

with open('input.txt') as f:
    root = Dir('', None)
    root.mkdir('/')

    curr_root = root
    for r in f:
        r = r.strip()
        if r.startswith('$'):
            _, cmd = r.split(maxsplit=1)
            if cmd.startswith('cd'):
                cmd, arg = cmd.split()
                if arg == '..':
                    curr_root = curr_root.parent
                else:
                    curr_root = curr_root[arg]
        elif r.startswith('dir'):
            d, name = r.split()
            curr_root.mkdir(name)
        else:  # entry is a file
            size, name = r.split()
            curr_root.touch(name, int(size))

    print('total size from /: {}'.format(root.size))
    mem_free = int(7e7-root.size)
    print('mem free: {}'.format(mem_free))
    space_reqd = int(3e7 - mem_free)
    print('addnl free space needed: {}'.format(space_reqd))

    res = walk(root, lambda x: x < 100000, [])
    total_size = 0
    for entry in res:
        total_size += entry.size
        #print(str(entry))

    print('total size of directories < 1e5: {}'.format(total_size))

    res = walk(root, lambda x: x > space_reqd, [])
    min_d = sorted(res, key=lambda d: d.size)[0]
    print('dir to delete: {}'.format(min_d))
