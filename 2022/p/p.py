from pprint import pprint
from queue import PriorityQueue
import re

PARSE_LINE = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnel(?:s?) lead(?:s?) to valve(?:s?) (.*)\n')


class Graph:
    def __init__(self):
        self.nodes = dict()

    def __getitem__(self, item):
        return self.nodes[item]

    def __iter__(self):
        return self.nodes.__iter__()

    def add_node(self, name, flow):
        self.nodes[name] = Node(name, flow)

    def add_edges(self, origin, connections):
        for connection in connections:
            self.nodes[origin].add_neighbor(connection)


class Node:
    def __init__(self, name, flow):
        self.name = name
        self.flow = flow
        self.open = False
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)


class Memo:
    def __init__(self):
        self.memo = dict()

    def __getitem__(self, item):
        # item is expected to be a tuple of:
        #   set of open valves
        #   current position
        #   time remaining
        #   other players still to go
        return self.memo[item]


def calc_distance(start, end, graph):
    visited = set()
    q = PriorityQueue()
    q.put((0, start))

    while not q.empty():
        cur = q.get()
        distance = cur[0]
        node_name = cur[1]

        if node_name in visited:
            continue

        visited.add(node_name)

        # found the end
        if node_name == end:
            return distance

        node = graph[node_name]

        for neighbor in node.neighbors:
            q.put((distance + 1, neighbor))

    print(f"Error finding path from {start} to {end}")
    return -1


def calc_distances(graph):
    distances = dict()
    for start_node in graph:
        # ignore 0 flow nodes that aren't our whole-problem start node
        if graph[start_node].flow == 0 and not graph[start_node].name == 'AA':
            continue

        distances[start_node] = dict()
        for end_node in graph:
            if not start_node == end_node and graph[end_node].flow > 0:
                distances[start_node][end_node] = calc_distance(start_node, end_node, graph)

    return distances


def dfs(current_node, graph, distances, closed, time_remaining):
    best = 0
    nodes_opened = set()

    if time_remaining <= 0 or len(closed) == 0:
        return best, nodes_opened

    for node in closed:
        # 1 minute per distance + 1 to turn on the valve
        time_used = distances[current_node][node] + 1
        current_time = time_remaining - time_used
        pressure_relieved, nodes_used = dfs(node, graph, distances, (closed - {node}), current_time)
        pressure_relieved += current_time * graph[node].flow
        if pressure_relieved > best:
            best = pressure_relieved
            nodes_opened = nodes_used
            nodes_opened.add(node)

    return best, nodes_opened


def memo_dfs(current_node, graph, distances, opened, time_remaining, other_players, time_limit, start, memo, bitmap):
    # restart the dfs if we're out of time for the current player
    if time_remaining <= 0:
        if other_players == 0:
            return 0
        else:
            return memo_dfs(start, graph, distances, opened, time_limit, other_players - 1, time_limit, start, memo, bitmap)

    # bail search early if we've been here before
    bits = convert_set_to_bitmap(opened, bitmap)
    state = (current_node, bits, time_remaining, other_players)
    if state in memo:
        return memo[state]

    best = 0
    for node in distances[current_node]:
        if node in opened:
            continue

        new_time = time_remaining - (distances[current_node][node] + 1)
        new_opened = opened
        pressure_relieved = 0
        if new_time > 0:
            new_opened = new_opened | {node}
            pressure_relieved = new_time * graph[node].flow
        pressure_relieved += memo_dfs(node, graph, distances, new_opened, new_time, other_players, time_limit, start, memo, bitmap)
        best = max(best, pressure_relieved)

    # check the "stop playing here" state
    if other_players > 0:
        pressure_relieved = memo_dfs(start, graph, distances, opened, time_limit, other_players - 1, time_limit, start, memo, bitmap)
        best = max(best, pressure_relieved)

    memo[state] = best
    return best


def convert_set_to_bitmap(nodes, bitmap):
    val = 0
    for node in nodes:
        val |= (1 << bitmap[node])
    return val


def relieve_pressure(graph, distances, start, time_limit):
    closed_nodes = set([node for node in graph if graph[node].flow > 0])
    pressure_relieved, _ = dfs(start, graph, distances, closed_nodes, time_limit)
    return pressure_relieved


def relive_pressure_pt2(graph, distances, start, time_limit, bitmap):
    return memo_dfs(start, graph, distances, set(), time_limit, 1, time_limit, start, dict(), bitmap)


def parse(filename):
    graph = Graph()
    bitmap = dict()
    idx = 0
    with open(filename, 'r') as file:
        for line in file:
            m = re.match(PARSE_LINE, line)
            graph.add_node(m[1], int(m[2]))
            graph.add_edges(m[1], m[3].split(', '))
            bitmap[m[1]] = idx
            idx += 1
    return graph, bitmap


def main():
    test = False
    filename = "./p/input.txt"

    if test:
        filename = "./p/test.txt"

    graph, bitmap = parse(filename)

    # calculate distance from all non-0 nodes + AA to all other non-zero nodes
    distances = calc_distances(graph)

    print(f"Part 1: {relieve_pressure(graph, distances, 'AA', 30)}")
    print(f"Part 2: {relive_pressure_pt2(graph, distances, 'AA', 26, bitmap)}")


if __name__ == "__main__":
    main()
