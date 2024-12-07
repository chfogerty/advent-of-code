UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DIRECTION_VECS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Guard:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.dir = UP
    
    def get_pos(self):
        return (self.row, self.col)
    
    def set_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]
    
    def next_pos(self):
        direction = DIRECTION_VECS[self.dir]
        return (self.row + direction[0], self.col + direction[1])
    
    def move(self):
        next_pos = self.next_pos()
        self.row = next_pos[0]
        self.col = next_pos[1]

    def next_dir(self):
        # rotate 90
        return (self.dir + 1) % 4
    
    def rotate(self):
        self.dir = self.next_dir()
    
    def __str__(self):
        return f"({self.row}, {self.col}), {self.dir}"

def in_bounds(position, room_size):
    return position[0] < room_size[0] and position[0] >= 0 and position[1] < room_size[1] and position[1] >= 0


def simulate_guard(guard, obstacles, room_size):
    positions = set()

    while in_bounds(guard.get_pos(), room_size):
        positions.add(guard.get_pos())
        next_pos = guard.next_pos()
        if next_pos in obstacles:
            guard.rotate()
        else:
            guard.move()

    return len(positions)

def parse(filename):
    obstacles = set()
    guard = Guard()
    size = (0, 0)
    with open(filename, 'r') as file:
        rows = 0
        cols = 0
        for line in file:
            if cols == 0:
                cols = len(line.rstrip())
            
            for idx in range(len(line)):
                c = line[idx]
                if c == '#':
                    obstacles.add((rows, idx))
                if c == '^':
                    guard.set_pos((rows, idx))
            rows += 1
        size = (rows, cols)
    return (obstacles, guard, size)


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    obstacles, guard, size = parse(filename)
    print(simulate_guard(guard, obstacles, size))