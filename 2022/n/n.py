def inclusive_range(start, end, increment=1):
    return range(start, end+1, increment)


def order_corners(a, b):
    if a[0] > b[0] or a[1] > b[1]:
        return (b, a)
    return (a, b)


def parse(filename):
    shapes = []
    with open(filename, 'r') as file:
        for raw_line in file:
            line = raw_line.strip()
            corners = [(int(txt.split(',')[0]), int(txt.split(',')[1])) for txt in line.split(" -> ")]
            shapes.append(corners)
    return shapes


def create_rocks(shapes):
    rocks = set()
    min_x = 1000
    max_x = -1
    max_y = -1
    for shape in shapes:
        for corner_idx in range(1, len(shape)):
            low, high = order_corners(shape[corner_idx - 1], shape[corner_idx])
            x_range = list(inclusive_range(low[0], high[0]))
            y_range = list(inclusive_range(low[1], high[1]))
            min_x = min([min_x, min(x_range)])
            max_x = max([max_x, max(x_range)])
            max_y = max([max_y, max(y_range)])
            x_count = len(x_range)
            y_count = len(y_range)
            x_range = x_range * y_count
            y_range = y_range * x_count
            for rock in zip(x_range, y_range):
                rocks.add(rock)
    return (rocks, (min_x, 0), (max_x, max_y))


def update_sand_loc(rocks, sand_loc, floor):
    if sand_loc[1] + 1 == floor:
        return (sand_loc, False)
    if (sand_loc[0], sand_loc[1] + 1) not in rocks:
        return ((sand_loc[0], sand_loc[1] + 1), True)
    if (sand_loc[0] - 1, sand_loc[1] + 1) not in rocks:
        return ((sand_loc[0] - 1, sand_loc[1] + 1), True)
    if (sand_loc[0] + 1, sand_loc[1] + 1) not in rocks:
        return ((sand_loc[0] + 1, sand_loc[1] + 1), True)
    return (sand_loc, False)


def pt1_endcon(sand_loc, top_left, bottom_right, _):
    return sand_loc[0] < top_left[0] or sand_loc[0] > bottom_right[0] or sand_loc[1] > bottom_right[1]


def pt2_endcon(sand_loc, _tl, _br, sand_start):
    return sand_loc[0] == sand_start[0] and sand_loc[1] == sand_start[1]


def simulate_sand(rocks, top_left, bottom_right, sand_start, endcon, floor=-1):
    done = False
    grains = 0
    while not done:
        sand_loc = (sand_start[0], sand_start[1])
        falling = True
        while falling:
            sand_loc, falling = update_sand_loc(rocks, sand_loc, floor)
            # bounds check
            if endcon(sand_loc, top_left, bottom_right, sand_start):
                falling = False
                done = True
        if not done:
            grains += 1
            rocks.add(sand_loc)

    return grains


def main():
    test = False
    filename = "./n/input.txt"

    if test:
        filename = "./n/test.txt"
    rocks, top_left, bottom_right = create_rocks(parse(filename))
    print(simulate_sand(rocks, top_left, bottom_right, (500, 0), pt1_endcon))

    rocks, top_left, bottom_right = create_rocks(parse(filename))
    print(simulate_sand(rocks, top_left, bottom_right, (500, 0), pt2_endcon, bottom_right[1] + 2) + 1)


if __name__ == "__main__":
    main()
