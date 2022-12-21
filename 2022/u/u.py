import re


class Monkey:
    def __init__(self, name, func, operands=None):
        self.name = name
        self.func = func
        self.operands = operands

        if operands is None:
            self.result = self.func()
        else:
            self.result = None

    def execute(self, monkeys):
        if self.result is not None:
            return self.result

        a = monkeys[self.operands[0]].execute(monkeys)
        b = monkeys[self.operands[1]].execute(monkeys)

        return self.func(a, b)


def add(a, b):
    return a+b


def sub(a, b):
    return a-b


def mul(a, b):
    return a*b


def div(a, b):
    return a/b


def eq(a, b):
    return a - b


def parse(filename, part2=False):
    monkeys = dict()

    with open(filename, 'r') as file:
        for raw_line in file:
            line = raw_line.strip()
            name_op_split = line.split(': ')
            name = name_op_split[0]
            operands = None
            func = lambda *args: None

            if m := re.match(EXTRACT_OPERANDS, name_op_split[1]):
                operands = [m.group(1), m.group(3)]
                func = FUNCTION_MAP[m.group(2)]
            else:
                result = int(name_op_split[1])
                func = lambda *args: result

            if part2 and name == 'root':
                func = eq

            monkeys[name] = Monkey(name, func, operands)
    return monkeys


def find_humn(monkeys):
    stack = [monkeys['root'].operands[0]]
    while len(stack) > 0:
        monkey = stack.pop()
        if monkey == 'humn':
            return True

        if monkeys[monkey].operands:
            stack.append(monkeys[monkey].operands[0])
            stack.append(monkeys[monkey].operands[1])

    return False


EXTRACT_OPERANDS = re.compile('(.{4}) ([+-/*]) (.{4})')
FUNCTION_MAP = {'+': add, '-': sub, '*': mul, '/': div}


def main():
    test = False
    part2 = True
    filename = "./u/input.txt"

    if test:
        filename = "./u/test.txt"

    monkeys = parse(filename, part2)

    if not part2:
        print(monkeys['root'].execute(monkeys))
    else:
        space = (0, 99999999999999)
        mid = 0
        result = monkeys['root'].execute(monkeys)
        initial_sign = result < 0
        while not result == 0:
            print(result, monkeys['humn'].result, space)
            mid = sum(space) // 2
            monkeys['humn'].result = mid
            result = monkeys['root'].execute(monkeys)
            if (result > 0 and initial_sign) or (result < 0 and not initial_sign):
                space = (space[0], mid)
            else:
                space = (mid + 1, space[1])
        print(result, mid)


if __name__ == "__main__":
    main()
