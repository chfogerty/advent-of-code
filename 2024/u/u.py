NUM_PAD = {'7': (0, 0), '8': (0, 1), '9': (0, 2), '4': (1, 0), '5': (1, 1), '6': (1, 2), '1': (2, 0), '2': (2, 1), '3': (2, 2), '0': (3, 1), 'A': (3, 2)}
DIR_PAD = {(-1, 0): (0, 1), 'A': (0, 2), (0, -1): (1, 0), (1, 0): (1, 1), (0, 1): (1, 2)}
DIR_TO_KEY = {(-1, 0): '^', 'A': 'A', (0, -1): '<', (1, 0): 'v', (0, 1): '>'}

GRAM_MEMO = dict()

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

# Some function that takes a sequence and loops over it, calling fn2 on each 2-gram in the sequence
def expand_sequence(sequence, depth, pad):
    if depth == 0:
        return len(sequence)

    expanded = expand_2gram('A', sequence[0], depth, pad)
    for idx in range(1, len(sequence)):
        expanded += expand_2gram(sequence[idx - 1], sequence[idx], depth, pad)
    return expanded

# Some function that, given a 2-gram, returns the minimum expanded sequence for that 2-gram
def expand_2gram(start_key, end_key, depth, pad):
    if depth == 0:
        GRAM_MEMO[(start_key, end_key, depth)] = 2
        return 2
    
    if (start_key, end_key, depth) in GRAM_MEMO:
        return GRAM_MEMO[(start_key, end_key, depth)]

    min_sequence = float('inf')
    for option in get_input_options(start_key, end_key, pad):
        min_sequence = min(min_sequence, expand_sequence(option, depth - 1, DIR_PAD))
    
    GRAM_MEMO[(start_key, end_key, depth)] = min_sequence
    return min_sequence

# Gets input options to go from start key to end key on pad when using a direcitonal pad to navigate
# Includes the final "enter" button as well to input the end key
def get_input_options(start_key, end_key, pad):
    if start_key == end_key:
        return [['A']]
    options = []
    start = pad[start_key]
    end = pad[end_key]
    dist = (end[0] - start[0], end[1] - start[1])
    vert_keys = []
    if dist[0] != 0:
        vert_keys = [(dist[0] // abs(dist[0]), 0)] * abs(dist[0])
    horiz_keys = []
    if dist[1] != 0:
        horiz_keys = [(0, dist[1] // abs(dist[1]))] * abs(dist[1])

    if add(start, (dist[0], 0)) in pad.values():
        options.append(vert_keys + horiz_keys + ['A'])
    if add(start, (0, dist[1])) in pad.values():
        options.append(horiz_keys + vert_keys + ['A'])

    return options

def key_number(door_key):
    return int(door_key[:-1])

def complexity(door_keys):
    total = 0
    for key in door_keys:
        num = key_number(key)
        length = expand_sequence(key, 26, NUM_PAD)
        total += num * length
    return total

def parse(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    door_keys = parse(filename)
    print(complexity(door_keys))