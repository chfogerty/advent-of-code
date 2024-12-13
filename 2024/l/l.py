def in_bounds(pos, size):
    return pos[0] < size[0] and pos[0] >= 0 and pos[1] < size[1] and pos[1] >= 0

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def gen_neighbors(pos, condition, dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]):
    neighbors = []
    for dir in dirs:
        neighbor = add(pos, dir)
        if condition(neighbor):
            neighbors.append(neighbor)
    return neighbors

def find_fences(grid):
    size = (len(grid), len(grid[0]))
    fences = [[4 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for r in range(size[0]):
        for c in range(size[1]):
            condition = lambda n: in_bounds(n, size) and grid[r][c] == grid[n[0]][n[1]]
            # only search down and to the left
            neighbors = gen_neighbors((r, c), condition, dirs=[(1, 0), (0, 1)])
            for neighbor in neighbors:
                fences[neighbor[0]][neighbor[1]] -= 1
            fences[r][c] -= len(neighbors)
    return fences

def find_sides(region, grid):
    corners = 0
    corner_dirs = [
        [(-1, 1), (-1, 0), (0, 1)],
        [(1, 1), (0, 1), (1, 0)],
        [(1, -1), (1, 0), (0, -1)],
        [(-1, -1), (0, -1), (-1, 0)]
    ]
    size = (len(grid), len(grid[0]))
    for plot in region:
        for dirs in corner_dirs:
            condition = lambda n: in_bounds(n, size) and grid[plot[0]][plot[1]] == grid[n[0]][n[1]]
            diagonal = add(plot, dirs[0])
            neighbors = gen_neighbors(plot, condition, dirs[1:])
            corner = len(neighbors) == 0 or (diagonal not in region and len(neighbors) % 2 == 0)
            if corner:
                corners += 1
    return corners


def find_region(start, grid, size):
    region = set()
    stack = [start]
    while len(stack) > 0:
        pos = stack.pop()
        if pos in region:
            continue

        region.add(pos)
        condition = lambda n: in_bounds(n, size) and grid[pos[0]][pos[1]] == grid[n[0]][n[1]]
        neighbors = gen_neighbors(pos, condition)
        stack.extend(neighbors)
    return region


def find_regions(grid):
    visited = set()
    regions = []
    size = (len(grid), len(grid[0]))

    for r in range(size[0]):
        for c in range(size[1]):
            if (r, c) not in visited:
                regions.append(find_region((r, c), grid, size))
                visited.update(regions[-1])
    return regions

def price_grid(regions, fences):
    total = 0
    for region in regions:
        area = len(region)
        perimeter = sum([fences[plot[0]][plot[1]] for plot in region])
        total += area * perimeter
    return total

def discount_grid(regions, grid):
    total = 0
    for region in regions:
        area = len(region)
        sides = find_sides(region, grid)
        total += area * sides
    return total

def parse(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            row = [c for c in line.strip()]
            grid.append(row)
    return grid

def pprint_grid(grid):
    for r in grid:
        s = ''
        for c in r:
            s += str(c)
        print(s)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    grid = parse(filename)
    fences = find_fences(grid)
    regions = find_regions(grid)

    print(price_grid(regions, fences))
    print(discount_grid(regions, grid))