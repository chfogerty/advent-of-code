from heapq import heappush, heappop

def in_bounds(pos, size):
    return pos[0] <= size[0] and pos[0] >= 0 and pos[1] <= size[1] and pos[1] >= 0

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

def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def a_star(start, goal, size, bad_locs):
    visited = set()
    prio_queue = []
    heappush(prio_queue, (heuristic(start, goal), start))
    g_score = dict()
    g_score[start] = 0

    while len(prio_queue) > 0:
        f, point = heappop(prio_queue)
        if point in visited:
            continue
        visited.add(point)
        if point == goal:
            return f

        for neighbor in gen_neighbors(point, size, lambda p: p not in bad_locs):
            if neighbor not in visited:
                g_score[neighbor] = g_score[point] + 1
                heappush(prio_queue, (g_score[neighbor] + heuristic(neighbor, goal), neighbor))
    return -1

def bin_search(start, goal, corrupted, initial_test):
    low = initial_test
    high = len(corrupted)
    result = 0

    while high - low > 1:
        mid = ((high - low) // 2) + low
        result = a_star(start, goal, goal, corrupted[:mid])
        if result > -1:
            low = mid
        else:
            high = mid
    return corrupted[mid]


def parse(filename):
    with open(filename, 'r') as file:
        first = int(file.readline().strip())
        raw_data = file.read()
        data = [(int(x), int(y)) for s in raw_data.strip().split('\n') for (x, y) in [s.strip().split(',')]]
        return first, data[0], data[1:]

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    first, grid_size, corrupted = parse(filename)
    print(a_star((0, 0), grid_size, grid_size, corrupted[:first]))
    print(bin_search((0, 0), grid_size, corrupted, first))