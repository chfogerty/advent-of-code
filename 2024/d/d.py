NEXT_LETTERS = {'X': 'M', 'M': 'A', 'A': 'S'}
DIRECTION = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

def get_word(grid, locs):
    s = ""
    for loc in locs:
        s += grid[loc[0]][loc[1]]
    return s

def validate_locs(grid, locs):
    for loc in locs:
        if loc[0] < 0 or loc[0] >= len(grid) or loc[1] < 0 or loc[1] >= len(grid[loc[0]]):
            return False
    return True

def gen_locs(loc, direction, length=4):
    locs = [loc]
    while len(locs) < length:
        locs.append(add_tuple(locs[-1], direction))
    return locs

def gen_locs_x_mas(loc):
    locs = []
    # negative diagonal
    locs.append([add_tuple(loc, (-1, -1)), loc, add_tuple(loc, (1, 1))])
    # positive diagonal
    locs.append([add_tuple(loc, (1, -1)), loc, add_tuple(loc, (-1, 1))])
    return locs

def search(grid, loc, direction):
    locs = gen_locs(loc, direction)
    if not validate_locs(grid, locs):
        return 0
    word = get_word(grid, locs)
    if word == 'XMAS':
        return 1
    return 0

def find_xmas(grid):
    total = 0
    for r in range(0, len(grid)):
        for c in range(0, len(grid[r])):
            if grid[r][c] == 'X':
                for direction in DIRECTION:
                    total += search(grid, (r, c), direction)
    return total

def check_loc_x_mas(grid, x):
    for diag in x:
        if not validate_locs(grid, diag):
            return False
        word = get_word(grid, diag)
        if word != "MAS" and word != "SAM":
            return False
    return True


def find_x_mas(grid):
    total = 0
    for r in range(0, len(grid)):
        for c in range(0, len(grid[r])):
            if grid[r][c] == 'A':
                x = gen_locs_x_mas((r, c))
                if check_loc_x_mas(grid, x):
                    total += 1
    return total

def add_tuple(tup1, tup2):
    return(tup1[0]+tup2[0], tup1[1]+tup2[1])

def scale_tuple(tup, scale):
    return (tup[0]*scale, tup[1]*scale)


def parse(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append([])
            for c in line:
                grid[-1].append(c)
    return grid

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    grid = parse(filename)
    print(find_xmas(grid))
    print(find_x_mas(grid))