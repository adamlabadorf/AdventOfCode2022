class Item(object):
    def __init__(self, val):
        self.val = val
        self.id = id
    def __repr__(self):
        return 'Item({})'.format(hex(self.val))


class Monkey(object):
    def __init__(self, id):
        self.id = id
        self._items = []
        self.op = lambda x: x
        self.reduce = lambda x: x
        self.test = lambda x: True
        self.inspected = 0
        # must set these to monkeys manually
        self.monkey_true = self.monkey_false = None

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = [Item(_) for _ in items]
        self._init_items = [Item(_) for _ in items]

    def do_turn(self):
        for item in self.items:
            self.inspected += 1
            item.val = self.op(item.val)
            item.val = self.reduce(item.val)
            if self.test(item.val):
                self.monkey_true.catch(item)
            else:
                self.monkey_false.catch(item)
        self._items = []

    def catch(self, item):
        self._items.append(item)

with open('input.txt') as f:
    monkeys = []
    divisor_prod = 1
    for r in f:
        r = r.strip()
        if r.startswith('Monkey'):
            monkeys.append(Monkey(len(monkeys)))
        elif r.startswith('Starting'):
            _, items = r.split(':')
            monkeys[-1].items = [int(_) for _ in items.split(',')]
        elif r.startswith('Operation'):
            _, op = r.split('=')
            op = compile(op.strip(), '<string>', 'eval')
            def f(op):
                def g(old):
                    return eval(op)
                return g
            monkeys[-1].op = f(op)
        elif r.startswith('Test'):
            test = r.split(' ')
            def f(val):
                def g(x):
                    return (x % val) == 0
                return g
            divisor = int(test[-1])
            monkeys[-1].test = f(divisor)
            divisor_prod *= divisor
        elif r.startswith('If true'):
            test = r.split(' ')
            monkeys[-1].monkey_true = int(test[-1])
        elif r.startswith('If false'):
            test = r.split(' ')
            monkeys[-1].monkey_false = int(test[-1])

    # part 1, reduce for all monkeys is x/3
    # reduce = lambda x: x/3
    # part 2, reduce for all monkeys is x % <product of all divisors>
    def f(val):
        def g(x):
            return x % val
        return g
    reduce = f(divisor_prod)

    # monkey_true and monkey_false above were place holders
    # set them to the appropriate monkeys
    for monkey in monkeys:
        monkey.reduce = reduce
        monkey.monkey_true = monkeys[monkey.monkey_true]
        monkey.monkey_false = monkeys[monkey.monkey_false]

    for round in range(10000):
        for monkey in monkeys:
            monkey.do_turn()

        if round in (0, 19, 499, 799)+tuple(range(1999, 10000, 1000)):
            print('== After round {} =='.format(round+1))
            for monkey in monkeys:
                print('Monkey {} ({}): {}'.format(monkey.id, monkey.inspected, monkey.items))

    top_monkeys = sorted(monkeys, key=lambda m: m.inspected)[::-1]
    for monkey in top_monkeys:
        print('Monkey {} inspected items {} times.'.format(monkey.id, monkey.inspected))

    print('Monkey business: {}'.format(top_monkeys[0].inspected*top_monkeys[1].inspected))