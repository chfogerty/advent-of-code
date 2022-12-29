from enum import Enum


LEFT = -1
RIGHT = 1


HLINE = 0
CROSS = 1
L = 2
VLINE = 3
BLOCK = 4
ROCK_COUNT = 5


def parse(filename):
    with open(filename, 'r') as file:
        for line in file:
            return line.strip()


def create_rock(rock_type, high_point):
    bottom = high_point + 4
    if rock_type == HLINE:
        return ((2, bottom), (3, bottom), (4, bottom), (5, bottom))
    if rock_type == CROSS:
        return ((2, bottom + 1), (3, bottom + 2), (3, bottom + 1), (3, bottom), (4, bottom + 1))
    if rock_type == L:
        return ((2, bottom), (3, bottom), (4, bottom), (4, bottom + 1), (4, bottom + 2))
    if rock_type == VLINE:
        return ((2, bottom), (2, bottom + 1), (2, bottom + 2), (2, bottom + 3))
    if rock_type == BLOCK:
        return ((2, bottom), (3, bottom), (2, bottom + 1), (3, bottom + 1))


def move_rock(direction, rock, tower):
    new_rock = []
    for segment in rock:
        new_segment = (segment[0] + direction[0], segment[1] + direction[1])

        if new_segment in tower or new_segment[0] < 0 or new_segment[0] > 6 or new_segment[1] <= 0:
            # tower is 7 wide (0 to 6 incluseive), and two blocks can't be in the same spot
            # Additionally, the "floor" counts as layer 0, so we can't move into or below that.
            # do nothing if we're trying to move but are blocked
            return rock, True

        new_rock.append(new_segment)
    return tuple(new_rock), False


def apply_jet(direction, rock, tower):
    return move_rock((direction, 0), rock, tower)


def fall(rock, tower):
    return move_rock((0, -1), rock, tower)


def simulate_rock(current_jet, gas_jets, rock, tower, rock_num=1):
    settled = False
    while not settled:
        # gas jet
        direction = LEFT if gas_jets[current_jet] == '<' else RIGHT
        rock, _ = apply_jet(direction, rock, tower)
        current_jet = (current_jet + 1) % len(gas_jets)

        # fall
        rock, settled = fall(rock, tower)

    high_point = 0
    for segment in rock:
        high_point = max(high_point, segment[1])
        tower.add(segment)

    return high_point, current_jet


def trim_tower(tower, delta):
    high_points = []

    for x in range(0, 7):
        points = [0]
        points.extend([point[1] for point in tower if point[0] == x])
        high_point = max(points)
        high_points.append(high_point)

    to_remove = set()
    for point in tower:
        if high_points[point[0]] - delta > point[1]:
            to_remove.add(point)

    tower.difference_update(to_remove)

    return tuple(high_points)


def normalize_high_points(high_points):
    low = min(high_points)
    normalized_points = []
    for high_point in high_points:
        normalized_points.append(high_point - low)
    return tuple(normalized_points), low


def update_tower(tower, base_delta):
    new_tower = set()
    for segment in tower:
        new_tower.add((segment[0], segment[1] + base_delta))
    return new_tower


def tetris(filename, blocks):
    gas_jets = parse(filename)
    current_jet = 0
    rock_type = HLINE
    tower = set()
    high_point = 0
    block = 0
    # all values here are pre rock fall
    # key is (normalized high points, rock type, current jet)
    # value is (block, base for normalized high points)
    memo = dict()
    # key is same as above
    # value is (blocks to jump, base value increase)
    cycle = dict()

    # will need to be a while loop
    # for idx in range(0, blocks):
    while block < blocks:
        raw_high_points = trim_tower(tower, 100)
        high_points, base = normalize_high_points(raw_high_points)
        rock = create_rock(rock_type, high_point)
        key = (high_points, rock_type, current_jet)
        if key in cycle and cycle[key][0] + block < blocks:
            # handle cycle
            iterations_of_cycle = (blocks - block) // cycle[key][0]
            # update block
            block += (cycle[key][0] * iterations_of_cycle)
            # update base
            base += (cycle[key][1] * iterations_of_cycle)
            # update tower set to reflect new base
            tower = update_tower(tower, (cycle[key][1] * iterations_of_cycle))
            # update high point
            high_point += (cycle[key][1] * iterations_of_cycle)
        elif key in memo and key not in cycle:
            # detected cycle
            # do nothing to block, will handle on next loop in the above branch
            cycle[key] = (block - memo[key][0], base - memo[key][1])
        else:
            memo[key] = (block, base)
            rock_high_point, current_jet = simulate_rock(current_jet, gas_jets, rock, tower, block + 1)
            high_point = max(high_point, rock_high_point)
            rock_type = (rock_type + 1) % ROCK_COUNT
            block += 1

    return high_point


def pt1(filename):
    gas_jets = parse(filename)
    current_jet = 0
    rock_type = HLINE
    tower = set()
    high_point = 0

    for idx in range(0, 2022):
        trim_tower(tower, 100)
        rock = create_rock(rock_type, high_point)
        rock_high_point, current_jet = simulate_rock(current_jet, gas_jets, rock, tower, idx + 1)
        high_point = max(high_point, rock_high_point)
        rock_type = (rock_type + 1) % ROCK_COUNT

    return high_point


def main():
    test = False
    filename = "./q/input.txt"

    if test:
        filename = "./q/test.txt"

    print(pt1(filename))
    print(tetris(filename, 1000000000000))


if __name__ == "__main__":
    main()
