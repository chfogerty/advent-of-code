from pprint import pprint
from math import lcm


class Monkey:
    def __init__(self):
        self.items = []
        self.op_str = ""
        self.test = 1
        self.targets = dict()
        self.inspection_count = 0

    def set_op(self, s):
        self.op = eval(f"lambda old: {s}")

    def set_test(self, test):
        self.test = test

    def add_target(self, key, val):
        self.targets[key] = val

    def init_items(self, items):
        self.items = items

    def inspect_items(self, monkeys, manage_worry):
        while len(self.items) > 0:
            item = self.items.pop(0)
            item = self.op(item)
            item = manage_worry(item)
            target = self.targets[item % self.test == 0]
            monkeys[target].add_item(item)
            self.inspection_count += 1

    def add_item(self, item):
        self.items.append(item)

    def __str__(self):
        return ", ".join([str(item) for item in self.items])

    def __repr__(self):
        s = f"  Starting items: {str(self)}\n"
        s += f"  Operation: new = {self.op_str}\n"
        s += f"  Test: divisible by {self.test}\n"
        s += f"    If true: throw to monkey {self.targets[True]}\n"
        s += f"    If false: throw to monkey {self.targets[False]}\n"
        return s


def parse_monkeys(filename):
    monkeys = []
    with open(filename, 'r') as file:
        for l in file:
            line = l.strip()
            if l[0] == 'M':
                monkeys.append(Monkey())
            elif "Starting items:" in line:
                monkeys[-1].init_items([int(x) for x in line[16:].split(", ")])
            elif "Operation:" in line:
                monkeys[-1].set_op(line.split(" = ")[1])
            elif "Test:" in line:
                monkeys[-1].set_test(int(line.split()[-1]))
            elif "If true:" in line:
                monkeys[-1].add_target(True, int(line.split()[-1]))
            elif "If false:" in line:
                monkeys[-1].add_target(False, int(line.split()[-1]))
    return monkeys


def keep_away(rounds, monkeys, manage_worry):
    for i in range(0, rounds):
        for monkey in monkeys:
            monkey.inspect_items(monkeys, manage_worry)


def pt1(filename):
    monkeys = parse_monkeys(filename)
    keep_away(20, monkeys, lambda x: x // 3)
    ordered = [m.inspection_count for m in monkeys]
    ordered.sort()
    print(ordered[-1] * ordered[-2])


def pt2(filename):
    monkeys = parse_monkeys(filename)
    mod = lcm(*[monkey.test for monkey in monkeys])
    keep_away(10000, monkeys, lambda x: x % mod)
    ordered = [m.inspection_count for m in monkeys]
    ordered.sort()
    print(ordered[-1] * ordered[-2])


def main():
    test = False
    filename = "./k/input.txt"

    if test:
        filename = "./k/test.txt"

    pt1(filename)
    pt2(filename)


if __name__ == "__main__":
    main()
