from heapq import heappush, heappop

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def in_bounds(pos, size):
    return pos[0] < size[0] and pos[0] >= 0 and pos[1] < size[1] and pos[1] >= 0

def dijkstra(start, ends, graph):
    visited = dict()
    prio_queue = []
    heappush(prio_queue, (0, start, {start[:2]}))
    paths = set()
    best_dist = float('inf')
    while len(prio_queue) > 0:
        dist, state, path = heappop(prio_queue)
        if dist > best_dist:
            continue
        if state in ends:
            best_dist = dist
            paths.update(path)

        if state not in visited or visited[state] == dist:
            visited[state] = dist
            for neighbor in graph[state]:
                move_dist = dist + graph[state][neighbor]
                new_path = path.copy()
                new_path.add(neighbor[:2])
                heappush(prio_queue, (move_dist, neighbor, new_path))
    return best_dist, len(paths)

# a node in the graph is (r, c, facing)
# graph[a][b] gives the distance from state a to state b
def parse(filename):
    graph = dict()
    start = (0, 0, EAST)
    end = set()
    with open(filename, 'r') as file:
        lines = file.readlines()
        size = (len(lines), len(lines[0]))
        ortho = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for r in range(len(lines)):
            for c in range(len(lines[r])):
                if lines[r][c] == '#':
                    continue
                states = [(r, c, NORTH), (r, c, EAST), (r, c, SOUTH), (r, c, WEST)]
                if lines[r][c] == 'S':
                    start = states[EAST]
                if lines[r][c] == 'E':
                    end.update(states)
                for idx in range(len(states)):
                    state = states[idx]
                    graph[state] = dict()
                    cw = states[(idx + 1) % 4]
                    ccw = states[idx - 1]
                    graph[state][cw] = 1000
                    graph[state][ccw] = 1000
                    move = add(state[:2], ortho[state[2]])
                    if in_bounds(move, size) and lines[move[0]][move[1]] != '#':
                        graph[state][(move[0], move[1], state[2])] = 1
    return graph, start, end

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    graph, start, ends = parse(filename)
    best, seats = dijkstra(start, ends, graph)
    print(best, seats)