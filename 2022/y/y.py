import math
from collections import deque

FROM_SNAFU = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
TO_SNAFU = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}


def parse(filename):
    values = []
    with open(filename, 'r') as file:
        for line in file:
            val = 0
            for c in line.strip():
                val *= 5
                val += FROM_SNAFU[c]
            values.append(val)
    return values


def to_base5(fuel):
    base_5 = []
    while fuel > 0:
        base_5.append(fuel % 5)
        fuel = fuel // 5

    return base_5


def to_snafu_decimal(fuel):
    # digits = int(math.log(fuel, 5)) + 1
    base_5 = to_base5(fuel)
    base_5.append(0)

    for idx in range(0, len(base_5) - 1):
        if base_5[idx] > 2:
            base_5[idx] -= 5
            base_5[idx + 1] += 1

    if base_5[-1] == 0:
        base_5.pop()

    base_5.reverse()
    return base_5


def to_snafu(fuel):
    base_5 = to_snafu_decimal(fuel)
    snafu = [TO_SNAFU[digit] for digit in base_5]
    return ''.join(snafu)


def main():
    test = False
    filename = "./y/input.txt"

    if test:
        filename = "./y/test.txt"

    fuel = sum(parse(filename))
    print(to_snafu(fuel))


if __name__ == "__main__":
    main()
