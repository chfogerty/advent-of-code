def combo(operand, registers):
    if operand <= 3 and operand >=0:
        return operand
    if operand == 4:
        return registers['A']
    if operand == 5:
        return registers['B']
    if operand == 6:
        return registers['C']
    raise "Invalid Program"

def adv(registers, operand):
    combo_op = combo(operand, registers)
    registers['A'] = int(registers['A'] / (2.0 ** combo_op))
    return True

def bxl(registers, operand):
    registers['B'] = registers['B'] ^ operand
    return True

def bst(registers, operand):
    registers['B'] = combo(operand, registers) % 8
    return True

def jnz(registers, operand):
    if registers['A'] != 0:
        registers['PC'] = operand
        return False
    return True

def bxc(registers, operand):
    registers['B'] = registers['B'] ^ registers['C']
    return True

def out(registers, operand):
    combo_op = combo(operand, registers) % 8
    if 'OUT' not in registers:
        registers['OUT'] = str(combo_op)
    else:
        registers['OUT'] += f',{combo_op}'
    return True

def bdv(registers, operand):
    combo_op = combo(operand, registers)
    registers['B'] = int(registers['A'] / (2.0 ** combo_op))
    return True

def cdv(registers, operand):
    combo_op = combo(operand, registers)
    registers['C'] = int(registers['A'] / (2.0 ** combo_op))
    return True

OPS = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

def run(prog, registers):
    while registers['PC'] < len(prog):
        operator = prog[registers['PC']]
        if operator != 3 and registers['PC'] + 1 >= len(prog):
            return
        operand = prog[registers['PC'] + 1]
        inc = OPS[operator](registers, operand)
        if inc:
            registers['PC'] += 2

def rev_eng(prog):
    print(sorted(rev_eng_rec(0, prog, len(prog) - 1))[0])

def rev_eng_rec(a, prog, idx):
    if idx < 0:
        return [a]

    matches = []
    b_xor_c = prog[idx] ^ 7
    a = a << 3
    c = 0
    for pot_b in range(8):
        tmp = a | (pot_b ^ 2)
        c = tmp >> pot_b
        if ((pot_b ^ c) % 8) == b_xor_c:
            res = rev_eng_rec(tmp, prog, idx - 1)
            matches.extend(res)
    return matches

def parse(filename):
    registers = dict()
    registers['PC'] = 0
    prog = []
    with open(filename, 'r') as file:
        lines = file.read()
        reg_defs, prog = lines.strip().split('\n\n')
        for reg_def in reg_defs.split('\n'):
            _, reg, val = reg_def.split()
            registers[reg[0]] = int(val)
        prog = [int(x) for x in prog[8:].split(',')]
    return registers, prog

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    registers, prog = parse(filename)
    run(prog, registers)
    print(registers['OUT'])
    rev_eng(prog)