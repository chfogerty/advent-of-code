import re


def sum_tuples(*tuples):
    return tuple(map(lambda *args: sum(args), *tuples))


def parse(filename):
    *raw_grid, _, path = open(filename, 'r')
    x = raw_grid[0].index('.')
    y = 0
    dx = 1
    dy = 0
    grid = {(x, y): c for y, l in enumerate(raw_grid) for x, c in enumerate(l) if c in '.#'}
    return grid, (x, y), (dx, dy), re.findall(r'\d+|[LR]', path)


def flat_warp(pos, direction, grid):
    next_pos = sum_tuples(pos, direction)
    if next_pos not in grid:
        # the index for the coordinate we're not moving
        locked = 0 if direction[0] == 0 else 1

        # the index for the coordinate that we're moving along
        free = locked * -1 + 1

        line = [p for p in grid if p[locked] == next_pos[locked]]
        next_pos = min(line, key=lambda p: p[free] * direction[free])

    if grid[next_pos] == '#':
        return pos

    return next_pos


def update_cube_pos(pos, direction, grid):
    next_pos = sum_tuples(pos, direction)
    next_dir = direction
    if next_pos not in grid:
        next_pos, next_dir = warp(next_pos, direction)
    if grid[next_pos] == '.':
        return next_pos, next_dir

    return pos, direction


# assumption: we only call this when we need to warp
def warp(cur_pos, cur_dir):
    x_face = cur_pos[0] // 50
    y_face = cur_pos[1] // 50

    # only x or y matters because the other one will be invalid since we're warping
    match cur_dir, x_face, y_face:
        # left going up (to front)
        case(0, -1), 0, _: return (50, cur_pos[0] + 50), (1, 0)
        # top going up (to back)
        case(0, -1), 1, _: return (0, cur_pos[0] + 100), (1, 0)
        # right going up (to back)
        case(0, -1), 2, _: return (cur_pos[0] - 100, 199), (0, -1)
        # right going right (to bottom)
        case(1, 0), _, 0: return (49, 149 - cur_pos[1]), (-1, 0)
        # front going right (to right)
        case(1, 0), _, 1: return (cur_pos[1] + 50, 49), (0, -1)
        # bottom going right (to right)
        case(1, 0), _, 2: return (149, 149 - cur_pos[0]), (-1, 0)
        # back going right (to bottom)
        case(1, 0), _, 3: return (cur_pos[1] - 100, 149), (0, -1)
        # back going down (to right)
        case(0, 1), 0, _: return (cur_pos[0] + 100, 0), (0, 1)
        # bottom going down (to back)
        case(0, 1), 1, _: return (49, cur_pos[0] + 100), (-1, 0)
        # right going down (to front)
        case(0, 1), 2, _: return (99, cur_pos[0] - 50), (-1, 0)
        # top going left (to left)
        case(-1, 0), _, 0: return (0, 149 - cur_pos[1]), (1, 0)
        # front going left (to left)
        case(-1, 0), _, 1: return (cur_pos[1] - 50, 100), (0, 1)
        # left going left (to top)
        case(-1, 0), _, 2: return (50, 149 - cur_pos[1]), (1, 0)
        # back going left (to top)
        case(-1, 0), _, 3: return (cur_pos[1] - 100, 0), (0, 1)


def facing(direction):
    return [(1, 0), (0, 1), (-1, 0), (0, -1)].index(direction)


def pt1(filename):
    grid, pos, direction, path = parse(filename)

    for move in path:
        if move == 'L':
            direction = (direction[1], -1*direction[0])
        elif move == 'R':
            direction = (-1*direction[1], direction[0])
        else:
            for _ in range(int(move)):
                pos = flat_warp(pos, direction, grid)

    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing(direction)


def pt2(filename):
    grid, pos, direction, path = parse(filename)

    for move in path:
        if move == 'L':
            direction = (direction[1], -1*direction[0])
        elif move == 'R':
            direction = (-1*direction[1], direction[0])
        else:
            for _ in range(int(move)):
                pos, direction = update_cube_pos(pos, direction, grid)

    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing(direction)


def main():
    test = False
    filename = "./v/input.txt"

    if test:
        filename = "./v/test.txt"

    print(pt1(filename))
    print(pt2(filename))


if __name__ == "__main__":
    main()
