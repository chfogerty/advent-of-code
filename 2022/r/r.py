import math


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def gen_adjacent(cube):
    x = cube[0]
    y = cube[1]
    z = cube[2]

    adjacent = []
    for i in range(x-1, x+2, 2):
        adjacent.append((i, y, z))

    for i in range(y-1, y+2, 2):
        adjacent.append((x, i, z))

    for i in range(z-1, z+2, 2):
        adjacent.append((x, y, i))

    return adjacent


def surface_area_pt1(cubes):
    processed_cubes = set()
    area_pt1 = 0

    for cube in cubes:
        adjacent_cubes = gen_adjacent(cube)
        filled_adjacent = [c for c in adjacent_cubes if c in processed_cubes]
        sides_added = 6 - len(filled_adjacent)
        sides_removed = len(filled_adjacent)
        area_pt1 = area_pt1 - sides_removed + sides_added
        processed_cubes.add(cube)

    return area_pt1


def in_bounds(cube, start, end):
    return cube[0] >= start[0] and cube[1] >= start[1] and cube[2] >= start[2] and cube[0] <= end[0] and cube[1] <= end[1] and cube[2] <= end[2]


def surface_area_pt2(cubes):
    minx = min([cube[0] for cube in cubes]) - 1
    miny = min([cube[1] for cube in cubes]) - 1
    minz = min([cube[2] for cube in cubes]) - 1
    maxx = max([cube[0] for cube in cubes]) + 1
    maxy = max([cube[1] for cube in cubes]) + 1
    maxz = max([cube[2] for cube in cubes]) + 1
    start = (minx, miny, minz)
    end = (maxx, maxy, maxz)
    visited = set()

    area = 0
    stack = [start]
    while len(stack) > 0:
        cube = stack.pop()
        if cube in visited:
            continue
        visited.add(cube)
        adjacent_cubes = gen_adjacent(cube)
        for adjacent_cube in adjacent_cubes:
            if adjacent_cube in cubes:
                area += 1
            elif in_bounds(adjacent_cube, start, end):
                stack.append(adjacent_cube)
    return area


def parse(filename):
    cubes = set()
    with open(filename, 'r') as file:
        for raw_line in file:
            line = raw_line.strip()
            cube = line.split(',')
            cubes.add((int(cube[0]), int(cube[1]), int(cube[2])))
    return cubes


def main():
    test = False
    filename = "./r/input.txt"

    if test:
        filename = "./r/test.txt"

    cubes = parse(filename)
    print(surface_area_pt1(cubes))

    print(surface_area_pt2(cubes))


if __name__ == "__main__":
    main()
