from heapq import heappush, heappop

def cab_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def in_bounds(pos, size):
    return pos[0] < size[0] and pos[0] >= 0 and pos[1] < size[1] and pos[1] >= 0

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def gen_neighbors(pos, size, condition, directions):
    neighbors = []
    for dir in directions:
        neighbor = add(pos, dir)
        if in_bounds(neighbor, size) and condition(neighbor):
            neighbors.append(neighbor)
    return neighbors

def gen_next_neighbors(pos, size, condition):
    ortho = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return gen_neighbors(pos, size, condition, ortho)

# def a_star(start, goal, size, walls):
#     visited = set()
#     prio_queue = []
#     heappush(prio_queue, (heuristic(start, goal), start))
#     g_score = dict()
#     g_score[start] = 0

#     while len(prio_queue) > 0:
#         f, point = heappop(prio_queue)
#         if point in visited:
#             continue
#         visited.add(point)
#         if point == goal:
#             return f

#         for neighbor in gen_neighbors(point, size, lambda p: p not in walls):
#             if neighbor not in visited:
#                 g_score[neighbor] = g_score[point] + 1
#                 heappush(prio_queue, (g_score[neighbor] + heuristic(neighbor, goal), neighbor))
#     return -1

def bfs(start, goal, size, walls):
    visited = dict()
    prio_queue = []
    heappush(prio_queue, (0, start))

    cond = lambda p: p not in walls

    while len(prio_queue) > 0:
        dist, point = heappop(prio_queue)
        if point in visited:
            continue
        visited[point] = dist

        if point == goal:
            return visited

        for neighbor in gen_next_neighbors(point, size, cond):
            heappush(prio_queue, (dist + 1, neighbor))
    return visited

def find_shortcuts_2(base_path, size):
    shortcuts = []
    cheat_offsets = []
    for r in range(-2, 3, 1):
        for c in range(-2, 3, 1):
            total_dist = abs(r) + abs(c)
            if total_dist == 2:
                cheat_offsets.append((r, c))

    for point in base_path:
        condition = lambda p: p in base_path and base_path[p] > base_path[point] and cab_dist(p, point) != abs(base_path[p] - base_path[point])
        for neighbor in gen_neighbors(point, size, condition, cheat_offsets):
            # subtract 2 from the shortcut time because using the shortcut takes 2 moves
            shortcuts.append(base_path[neighbor] - base_path[point] - 2)
    return shortcuts

def find_shortcuts(base_path, size):
    shortcuts = []
    cheat_offsets = []
    for r in range(-20, 21, 1):
        for c in range(-20, 21, 1):
            total_dist = abs(r) + abs(c)
            if total_dist <= 20:
                cheat_offsets.append((r, c))

    for point in base_path:
        condition = lambda p: p in base_path and base_path[p] > base_path[point] and cab_dist(p, point) != abs(base_path[p] - base_path[point])
        for neighbor in gen_neighbors(point, size, condition, cheat_offsets):
            # subtract distance moved from shortcut time
            total_dist = cab_dist(point, neighbor)
            shortcuts.append(base_path[neighbor] - base_path[point] - total_dist)
    return shortcuts

def parse(filename):
    start = (0, 0)
    end = (0, 0)
    path = set()
    walls = set()
    size = None
    with open(filename, 'r') as file:
        lines = file.readlines()
        for r in range(len(lines)):
            line = lines[r].strip()
            if size == None:
                size = (len(lines), len(line))
            for c in range(len(line)):
                if line[c] == '#':
                    walls.add((r, c))
                else:
                    path.add((r, c))
                if line[c] == 'S':
                    start = (r, c)
                if line[c] == 'E':
                    end = (r, c)

    return start, end, path, walls, size

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    start, end, path, walls, size = parse(filename)
    base_path = bfs(start, end, size, walls)
    shortcuts_2 = find_shortcuts_2(base_path, size)
    print(len([x for x in shortcuts_2 if x >= 100]))
    shortcuts = find_shortcuts(base_path, size)
    print(len([x for x in shortcuts if x >= 100]))
