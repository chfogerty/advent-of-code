def in_bounds(pos, size):
    return pos[0] < size[0] and pos[0] >= 0 and pos[1] < size[1] and pos[1] >= 0

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def gen_neighbors(pos, size, condition):
    ortho = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dir in ortho:
        neighbor = add(pos, dir)
        if in_bounds(neighbor, size) and condition(neighbor):
            neighbors.append(neighbor)
    return neighbors

def create_metadata(grid):
    graph = dict()
    heightmap = dict()
    size = (len(grid), len(grid[0]))
    for row in range(size[0]):
        for col in range(size[1]):
            condition = lambda x: grid[x[0]][x[1]] == grid[row][col] - 1
            neighbors = gen_neighbors((row, col), size, condition)
            graph[(row, col)] = neighbors
            if grid[row][col] not in heightmap.keys():
                heightmap[grid[row][col]] = []
            heightmap[grid[row][col]].append((row, col))
    return graph, heightmap

def score_positions(graph, heightmap, heads, tails):
    pos_score = dict()
    trail_score = dict()
    for tail in tails:
        for neighbor in graph[tail]:
            if neighbor not in pos_score.keys():
                pos_score[neighbor] = set()
            pos_score[neighbor].add(tail)

            if neighbor not in trail_score.keys():
                trail_score[neighbor] = []
            trail_score[neighbor].append([tail])

    for height in range(8, -1, -1):
        for position in heightmap[height]:
            if position in pos_score.keys():
                for neighbor in graph[position]:
                    if neighbor not in pos_score.keys():
                        pos_score[neighbor] = set()
                    pos_score[neighbor].update(pos_score[position])
            if position in trail_score.keys():
                for neighbor in graph[position]:
                    if neighbor not in trail_score.keys():
                        trail_score[neighbor] = []
                    for trail in trail_score[position]:
                        trail_score[neighbor].append(trail + [position])

    pos_total = 0
    trail_total = 0
    for head in heads:
        if head in pos_score.keys():
            pos_total += len(pos_score[head])
            trail_total += len(trail_score[head])
    return pos_total, trail_total

def parse(filename):
    grid = []
    heads = set()
    tails = set()
    with open(filename, 'r') as file:
        row = 0
        for line in file:
            grid.append([])
            col = 0
            for c in line.strip():
                grid[-1].append(int(c))
                if c == '0':
                    heads.add((row, col))
                if c == '9':
                    tails.add((row, col))
                col += 1
            row += 1

    return grid, heads, tails

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    grid, heads, tails = parse(filename)
    graph, heightmap = create_metadata(grid)
    print(score_positions(graph, heightmap, heads, tails))