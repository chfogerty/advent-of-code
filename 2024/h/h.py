from itertools import combinations

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def in_bounds(pos, size):
    return pos[0] < size[0] and pos[0] >= 0 and pos[1] < size[1] and pos[1] >= 0

def find_harmonics(antennas, size):
    antinodes = set()
    for combo in combinations(antennas, 2):
        antinodes.add(combo[0])
        antinodes.add(combo[1])
        dist = sub(combo[0], combo[1])

        first = add(combo[0], dist)
        while in_bounds(first, size):
            antinodes.add(first)
            first = add(first, dist)

        second = sub(combo[1], dist)
        while in_bounds(second, size):
            antinodes.add(second)
            second = sub(second, dist)
    return antinodes


def find_antinodes(antennas, size):
    antinodes = set()
    for combo in combinations(antennas, 2):
        # find distance
        dist = sub(combo[0], combo[1])

        # find first point
        first = add(combo[0], dist)
        if in_bounds(first, size):
            antinodes.add(first)

        # find second point
        second = sub(combo[1], dist)
        if in_bounds(second, size):
            antinodes.add(second)
    return antinodes

def count_locations(frequencies, size, func):
    antinodes = set()
    for frequency in frequencies:
        antennas = frequencies[frequency]
        antinodes.update(func(antennas, size))
    return len(antinodes)

def parse(filename):
    frequencies = dict()
    row = 0
    max_col = 0
    with open(filename, 'r') as file:
        for line in file:
            col = 0
            for c in line.rstrip():
                if c != '.':
                    if c not in frequencies.keys():
                        frequencies[c] = []
                    frequencies[c].append((row, col))
                col += 1
            max_col = col
            row += 1
    return (frequencies, (row, max_col))

def print_grid(points, size):
    for r in range(size[0]):
        s = ''
        for c in range(size[1]):
            if (r, c) in points:
                s += '#'
            else:
                s += '.'
        print(s)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    frequencies, size = parse(filename)

    print(count_locations(frequencies, size, find_antinodes))
    print(count_locations(frequencies, size, find_harmonics))