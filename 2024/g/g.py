import re

NUMBER = re.compile(r'\d+')

def sum_possible(eqns):
    total = 0
    for eqn in eqns:
        if test(eqn[0], eqn[1]):
            total += eqn[0]
    return total


def test(target, operands):
    if (len(operands) == 1):
        return target == operands[0]

    if target < operands[-1]:
        return False
    
    plus = test(target, operands[:-2] + [operands[-2] + operands[-1]])
    if plus:
        return True

    mult = test(target, operands[:-2] + [operands[-2] * operands[-1]])
    if mult:
        return True

    concat = test(target, operands[:-2] + [int(str(operands[-1]) + str(operands[-2]))])
    return concat

def parse(filename):
    eqns = []

    with open(filename, 'r') as file:
        for line in file:
            numbers = [int(n) for n in NUMBER.findall(line)]
            operands = numbers[1:]
            operands.reverse()
            eqns.append((numbers[0], operands))

    return eqns

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    print(sum_possible(parse(filename)))