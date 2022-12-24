import re

REGEX = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')


def normalize(val):
    return int(val / abs(val))


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def points_between(a, b):
    return abs(a[0] - b[0]) + 1


def generate_covered_verts(scanner, radius, y=10, top_left=None, bottom_right=None):
    # how many moves it takes to get from scanner y to target y
    moved = abs((scanner[1] - y))

    # if we're too far away, we cover no verts on the targeted row
    if moved > radius:
        return []

    remaining_moves = radius - moved
    x_start = scanner[0] - remaining_moves
    x_end = scanner[0] + remaining_moves + 1
    if top_left is not None:
        x_start = max(top_left[0], x_start)
        x_end = min(bottom_right[0] + 1, x_end)

    # we can move remaining_moves left or right, plus we cover the square (scanner[0], y)
    x_range = range(x_start, x_end)
    y_range = [y] * len(x_range)

    return list(zip(x_range, y_range))


def in_bounds(point, top_left, bottom_right):
    return point[0] >= top_left[0] and point[1] >= top_left[1] and point[0] <= bottom_right[0] and point[1] <= bottom_right[1]


def interpolate(a, b):
    # assuming we only need to move each value 1
    x_dir = normalize(b[0] - a[0])
    y_dir = normalize(b[1] - a[1])
    return x_dir, y_dir


def does_overlap(point, scanners, overlaps):
    for scanner in overlaps:
        if manhattan_distance(point, scanner) <= scanners[scanner]:
            return True

    return False


def check_manhattan_circle(scanner, scanners, overlaps, bounds):
    radius = scanners[scanner] + 1
    left = (scanner[0] - radius, scanner[1])
    top = (scanner[0], scanner[1] - radius)
    right = (scanner[0] + radius, scanner[1])
    bottom = (scanner[0], scanner[1] + radius)

    cardinal = [left, top, right, bottom]

    for idx in range(0, len(cardinal)):
        print(f"  {idx}")
        start = cardinal[idx]
        end = cardinal[(idx + 1) % len(cardinal)]
        x_dir, y_dir = interpolate(start, end)
        point = start
        num_points = points_between(start, end) + 1
        for pnt in range(0, num_points):
            # print(f"    {pnt}/{num_points}")
            if not does_overlap(point, scanners, overlaps) and in_bounds(point, bounds[0], bounds[1]):
                return point
            point = (point[0] + x_dir, point[1] + y_dir)

    return None


def parse(filename):
    scanners = dict()
    beacons = set()
    overlaps = dict()
    with open(filename, 'r') as file:
        for line in file:
            result = re.match(REGEX, line)
            scanner = (int(result[1]), int(result[2]))
            beacon = (int(result[3]), int(result[4]))
            scanners[scanner] = manhattan_distance(scanner, beacon)
            beacons.add(beacon)
            overlap = []
            for other in overlaps:
                distance = manhattan_distance(scanner, other)
                if distance - scanners[scanner] - scanners[other] - 1 < 1:
                    overlap.append(other)
                    overlaps[other].append(scanner)
            overlaps[scanner] = overlap
    return scanners, beacons, overlaps


def pt1(scanners, beacons, y=10):
    covered = set()
    for scanner in scanners:
        covered.update(generate_covered_verts(scanner, scanners[scanner], y))
    covered.difference_update(beacons)
    return covered


def pt2(scanners, overlaps, bounds):
    ordered_scanners = sorted(scanners.keys(), key=lambda scnr: len(overlaps[scnr]), reverse=True)
    for scanner in ordered_scanners:
        point = check_manhattan_circle(scanner, scanners, overlaps[scanner], bounds)
        if point is not None:
            return point, 4000000 * point[0] + point[1]
    return None, 0


def main():
    test = False
    filename = "./o/input.txt"
    y = 2000000
    tl = (0, 0)
    br = (4000000, 4000000)

    if test:
        filename = "./o/test.txt"
        y = 10
        br = (20, 20)

    scanners, beacons, overlaps = parse(filename)
    covered = pt1(scanners, beacons, y)
    print(len(covered))

    print("Part 2")
    point, freq = pt2(scanners, overlaps, (tl, br))
    print(point, freq)


if __name__ == "__main__":
    main()
