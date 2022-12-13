from queue import PriorityQueue
from pprint import pprint
from copy import deepcopy

MAXLEN = 100000


class Node:
    def __init__(self, height, distance, end, loc, char):
        self.height = height
        self.distance = distance
        self.end = end
        self.loc = loc
        self.char = char

    def __str__(self):
        return f"{self.height} {self.distance} {self.end}"

    def __repr__(self):
        return self.__str__()


def parse(filename):
    grid = []
    start = ()
    end = ()
    with open(filename, 'r') as file:
        row = -1
        for line in file:
            row += 1
            col = -1
            grid.append([])
            for c in line:
                col += 1
                if c == 'S':
                    grid[-1].append(Node(0, MAXLEN, False, (row, col), c))
                    start = (row, col)
                elif c == 'E':
                    grid[-1].append(Node(25, MAXLEN, True, (row, col), c))
                    end = (row, col)
                elif not str(c).isspace():
                    grid[-1].append(Node(ord(c) - ord('a'), MAXLEN, False, (row, col), c))

    return (grid, start, end)


def shortest_path(grid, start_pos, uphill=True):
    # visited = set()
    q = PriorityQueue()
    # start_node = grid[start_pos[0]][start_pos[1]]
    q.put((0, start_pos))

    # loop while q isn't empty
    while not q.empty():
        # pull top off q
        cur = q.get()
        node = grid[cur[1][0]][cur[1][1]]

        # if we've already visited this node, do nothing
        if node.distance < MAXLEN:
            continue

        # check if node at position is the end. If so, we did it!
        if uphill and node.end:
            return cur[0]
        elif not(uphill) and node.height == 0:
            return cur[0]

        # update distance to current node
        node.distance = cur[0]

        # get valid neighbors
        # add valid neighbors to q with priority of this node's distance + 1
        if uphill:
            neighbors = get_neighbors(grid, cur[1][0], cur[1][1], lambda x: x <= node.height + 1)
            for neighbor in neighbors:
                q.put((node.distance + 1, neighbor))
        else:
            neighbors = get_neighbors(grid, cur[1][0], cur[1][1], lambda x: x >= node.height - 1)
            for neighbor in neighbors:
                q.put((node.distance + 1, neighbor))


def get_neighbors(grid, x, y, accept):
    height = grid[x][y].height
    neighbors = []
    if x-1 >= 0 and accept(grid[x-1][y].height):
        neighbors.append((x-1, y))
    if x+1 < len(grid) and accept(grid[x+1][y].height):
        neighbors.append((x+1, y))
    if y-1 >= 0 and accept(grid[x][y-1].height):
        neighbors.append((x, y-1))
    if y+1 < len(grid[x]) and accept(grid[x][y+1].height):
        neighbors.append((x, y+1))
    return neighbors


def main():
    test = False
    filename = "./l/input.txt"

    if test:
        filename = "./l/test.txt"

    grid, start, end = parse(filename)
    print(f"Part 1: {shortest_path(deepcopy(grid), start)}")
    print(f"Part 2: {shortest_path(deepcopy(grid), end, False)}")


if __name__ == "__main__":
    main()
