from collections import Counter
import math

# https://stackoverflow.com/questions/15347174/python-finding-prime-factors
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

class PrimeIndexedInt(object):
    def __init__(self, val):
        self.val
        factors = prime_factors(val)
        # factors keeps track of how many of each prime compose the number
        self.factors = Counter(factors)


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
            #print(item.prime_factors)
            item.val = self.op(item.val)
            #i = math.floor(i/3)
            if self.test(item.val):
                self.monkey_true.catch(item)
            else:
                self.monkey_false.catch(item)
        self._items = []

    def catch(self, item):
        self._items.append(item)

with open('test.txt') as f:
    monkeys = []
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
            monkeys[-1].test = f(int(test[-1]))
        elif r.startswith('If true'):
            test = r.split(' ')
            monkeys[-1].monkey_true = int(test[-1])
        elif r.startswith('If false'):
            test = r.split(' ')
            monkeys[-1].monkey_false = int(test[-1])

    # monkey_true and monkey_false above were place holders
    # set them to the appropriate monkeys
    for monkey in monkeys:
        monkey.monkey_true = monkeys[monkey.monkey_true]
        monkey.monkey_false = monkeys[monkey.monkey_false]

    for round in range(10000):
        for monkey in monkeys:
            monkey.do_turn()

        if round in (0, 19, 499, 799)+tuple(range(1999,10000,1000)):
            print('== After round {} =='.format(round+1))
            for monkey in monkeys:
                print('Monkey {} ({}): {}'.format(monkey.id, monkey.inspected, monkey.items))

    top_monkeys = sorted(monkeys, key=lambda m: m.inspected)[::-1]
    for monkey in top_monkeys:
        print('Monkey {} inspected items {} times.'.format(monkey.id, monkey.inspected))

    print('Monkey business: {}'.format(top_monkeys[0].inspected*top_monkeys[1].inspected))