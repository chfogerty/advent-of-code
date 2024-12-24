from collections import deque

def AND(a, b):
    return a & b

def OR(a, b):
    return a | b

def XOR(a, b):
    return a ^ b

class Gate:
    def __init__(self, fn, output, s):
        self.a = None
        self.b = None
        self.fn = fn
        self.output = output
        self.initial_output = output
        self.s = s

    def set_output(self, output):
        self.output = output
    
    def reset(self):
        self.a = None
        self.b = None
        self.output = self.initial_output

    def set_input(self, val):
        if self.a == None:
            self.a = val
            return None, self.output
        self.b = val
        return self.fn(self.a, self.b), self.output
    
    def __hash__(self):
        return self.s.__hash__()

    def __eq__(self, other):
        return other and self.s == other.s

    def __ne__(self, other):
        return not self.__eq__(other)

def simulate(wire_states, gates, starting_states):
    dq = deque(starting_states)
    while len(dq) > 0:
        wire = dq.popleft()
        for gate in gates[wire]:
            val, out = gate.set_input(wire_states[wire])
            if val is not None:
                dq.append(out)
                wire_states[out] = val

def get_z_val(zs, wire_states):
    val = 0
    for z in zs:
        val = val << 1
        val += wire_states[z]
    return val

def get_initial(wire_states, letter):
    val = 0
    for bit in range(44, -1, -1):
        name = f'{letter}{bit:02d}'
        wireval = wire_states[name]
        val = val << 1
        val += wireval
    return val

def check_structure(structure):
    carry_in = 'prt'
    for bit in range(1, 45):
        x = f'x{bit:02d}'
        y = f'y{bit:02d}'
        z = f'z{bit:02d}'
        in_pair = (x, y)
        raw_add = structure[in_pair]['XOR']
        raw_carry = structure[in_pair]['AND']
        out_pair = tuple(sorted([raw_add, carry_in]))
        zout = structure[out_pair]['XOR']
        if zout != z:
            print(zout)
        carry_check = structure[out_pair]['AND']
        carry_pair = tuple(sorted([raw_carry, carry_check]))
        carry_in = structure[carry_pair]['OR']

def parse(filename):
    starting_states = []
    wire_states = dict()
    gates = dict()
    structure = dict()
    z_wires = []
    with open(filename, 'r') as file:
        lines = file.read()
        initial_states, gate_defs = lines.strip().split('\n\n')
        for state in initial_states.split('\n'):
            wire, val = state.strip().split(': ')
            wire_states[wire] = int(val)
            starting_states.append(wire)
        for gd in gate_defs.split('\n'):
            in1, fn, in2, _, out = gd.strip().split(' ')
            if in1 not in gates:
                gates[in1] = []
            if in2 not in gates:
                gates[in2] = []
            if out not in gates:
                gates[out] = []

            gate = Gate(globals()[fn], out, gd.strip())
            gates[in1].append(gate)
            gates[in2].append(gate)
            wire_states[out] = None
            if out[0] == 'z':
                z_wires.append(out)
            
            # standardize alphabetical
            one = in1
            two = in2
            if in1 > in2:
                one = in2
                two = in1
            if (one, two) not in structure:
                structure[(one, two)] = dict()
            structure[(one, two)][fn] = out
    return wire_states, gates, sorted(z_wires, reverse=True), starting_states, structure

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    wire_states, gates, z_wires, starting_states, structure = parse(filename)
    simulate(wire_states, gates, starting_states)
    z = get_z_val(z_wires, wire_states)
    print(z)
    x = get_initial(wire_states, 'x')
    y = get_initial(wire_states, 'y')
    print(x + y)
    check_structure(structure)
    print(','.join(sorted(['fkb', 'z16', 'rqf', 'nnr', 'rdn', 'z31', 'rrn', 'z37'])))