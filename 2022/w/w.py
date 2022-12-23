from collections import deque

DIRECTIONS = {'N': (-1, 0), 'NE': (-1, 1), 'E': (0, 1), 'SE': (1, 1), 'S': (1, 0), 'SW': (1, -1), 'W': (0, -1), 'NW': (-1, -1)}


def parse(filename):
    grove = set()
    with open(filename, 'r') as file:
        row = 0
        for line in file:
            col = 0
            for c in line:
                if c == '#':
                    grove.add((row, col))
                col += 1
            row += 1
    return grove


def find_bounds(grove):
    min_row = min([x[0] for x in grove])
    min_col = min([x[1] for x in grove])
    max_row = max([x[0] for x in grove])
    max_col = max([x[1] for x in grove])
    return ((min_row, min_col), (max_row, max_col))


def print_grove(grove, border=0):
    bounds = find_bounds(grove)
    for row in range(bounds[0][0]-border, bounds[1][0]+1+border):
        s = ""
        for col in range(bounds[0][1]-border, bounds[1][1]+1+border):
            if (row, col) in grove:
                s += "#"
            else:
                s += "."
        print(s)


def add_positions(a, b):
    return (a[0] + b[0], a[1] + b[1])


def elf_adjacent(grove, pos, to_check=DIRECTIONS):
    for direction in to_check:
        loc = add_positions(pos, DIRECTIONS[direction])
        if loc in grove:
            return True
    return False


def round(grove, consider):
    # location: list of elves trying to go there
    new_locs = dict()
    moved = False

    # first half: propose direction to move
    for elf in grove:
        if elf_adjacent(grove, elf):
            for direction in consider:
                if not elf_adjacent(grove, elf, direction):
                    new_loc = add_positions(elf, DIRECTIONS[direction[0]])
                    if new_loc not in new_locs:
                        new_locs[new_loc] = []
                    new_locs[new_loc].append(elf)
                    break

    # second half: resolve conflicting proposals
    for new_loc in new_locs:
        # only move if one elf is moving to the new location
        if len(new_locs[new_loc]) == 1:
            grove.add(new_loc)
            grove.remove(new_locs[new_loc][0])
            moved = True
    return moved


def starting_directions():
    north = ('N', 'NE', 'NW')
    south = ('S', 'SE', 'SW')
    west = ('W', 'NW', 'SW')
    east = ('E', 'NE', 'SE')

    return deque([north, south, west, east])


def spread_out(grove, rounds=10):
    directions = starting_directions()
    rnd = 0
    moved = True
    while not(rnd == rounds) and moved:
        moved = round(grove, directions)
        directions.rotate(-1)
        rnd += 1
    return rnd


def count_empty(grove):
    bounds = find_bounds(grove)
    height = bounds[1][0] - bounds[0][0] + 1
    width = bounds[1][1] - bounds[0][1] + 1
    area = width * height
    return area - len(grove)


def main():
    test = False
    pt2 = True
    filename = "./w/input.txt"
    rounds = 10

    if pt2:
        rounds = -1

    if test:
        filename = "./w/test.txt"

    grove = parse(filename)
    ended_round = spread_out(grove, rounds)
    print(count_empty(grove), ended_round)


if __name__ == "__main__":
    main()
