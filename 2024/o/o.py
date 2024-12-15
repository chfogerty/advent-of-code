WALL = '#'
BOX = 'O'
LEFT_BOX = '['
RIGHT_BOX = ']'
BOT = '@'
EMPTY = '.'
UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

DIRS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}

def reverse(move):
    if move == UP:
        return DIRS[DOWN]
    if move == DOWN:
        return DIRS[UP]
    if move == LEFT:
        return DIRS[RIGHT]
    return DIRS[LEFT]

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def in_bounds(position, room_size):
    return position[0] < room_size[0] and position[0] >= 0 and position[1] < room_size[1] and position[1] >= 0

def can_move(grid, start, dir):
    pos = add(start, dir)
    size = (len(grid), len(grid[0]))
    updated_pos = [start]
    while in_bounds(pos, size):
        updated_pos.append(pos)
        if grid[pos[0]][pos[1]] == EMPTY:
            updated_pos.reverse()
            return updated_pos
        if grid[pos[0]][pos[1]] == WALL:
            return []
        pos = add(pos, dir)
    return []

def can_wide_move(grid, start, dir):
    row, col = add(start, dir)
    affected_cols = {col}
    updated_pos = set()
    while True:
        added_cols = set()
        removed_cols = set()
        done = True
        for pos in zip([row] * len(affected_cols), affected_cols):
            if grid[pos[0]][pos[1]] == WALL:
                return set()
            if grid[pos[0]][pos[1]] == EMPTY:
                removed_cols.add(pos[1])
            elif grid[pos[0]][pos[1]] == LEFT_BOX:
                done = False
                added_cols.add(pos[1] + 1)
                updated_pos.add((pos[0], pos[1] + 1))
            elif grid[pos[0]][pos[1]] == RIGHT_BOX:
                done = False
                added_cols.add(pos[1] - 1)
                updated_pos.add((pos[0], pos[1] - 1))
            updated_pos.add(pos)
        if done:
            return updated_pos
        if len(removed_cols) > 0:
            affected_cols -= removed_cols
        if len(added_cols) > 0:
            affected_cols.update(added_cols)
        row += dir[0]

def simulate(grid, moves, start):
    bot_pos = start
    for move in moves:
        dir = DIRS[move]
        movement = can_move(grid, bot_pos, dir)
        for idx in range(len(movement) - 1):
            to_r, to_c = movement[idx]
            from_r, from_c = movement[idx+1]
            grid[to_r][to_c] = grid[from_r][from_c]

        if len(movement) > 0:
            empty_r, empty_c = movement[-1]
            grid[empty_r][empty_c] = EMPTY
            bot_pos = add(bot_pos, dir)
    return grid

def simulate_wide(grid, moves, start):
    bot_pos = start
    for move in moves:
        dir = DIRS[move]
        rev_dir = reverse(move)
        movement = []
        if move == UP or move == DOWN:
            updated_poses = can_wide_move(grid, bot_pos, dir)
            grid_updates = dict()
            for updated_pos in updated_poses:
                prev_pos = add(updated_pos, rev_dir)
                if prev_pos in updated_poses:
                    grid_updates[updated_pos] = grid[prev_pos[0]][prev_pos[1]]
                else:
                    grid_updates[updated_pos] = EMPTY
            
            if len(updated_poses) > 0:
                grid_updates[bot_pos] = EMPTY
                bot_pos = add(bot_pos, dir)
                grid_updates[bot_pos] = BOT

            for update in grid_updates:
                grid[update[0]][update[1]] = grid_updates[update]
        else:
            movement = can_move(grid, bot_pos, dir)
            for idx in range(len(movement) - 1):
                to_r, to_c = movement[idx]
                from_r, from_c = movement[idx+1]
                grid[to_r][to_c] = grid[from_r][from_c]
            if len(movement) > 0:
                empty_r, empty_c = movement[-1]
                grid[empty_r][empty_c] = EMPTY
                bot_pos = add(bot_pos, dir)
    return grid

def calc_gps(grid, box=BOX):
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == box:
                total = total + (100 * r) + c
    return total

def parse(filename):
    grid = []
    moves = ''
    start = (0, 0)
    with open(filename, 'r') as file:
        lines = file.read()
        start, actions = lines.strip().split('\n\n')
        board = start.split('\n')
        for r in range(len(board)):
            grid.append([])
            for c in range(len(board[r])):
                grid[-1].append(board[r][c])
                if board[r][c] == BOT:
                    start = (r, c)
        moves = ''.join(actions.split('\n'))
    return grid, moves, start

def widen(ch):
    if ch == WALL:
        return WALL + WALL
    if ch == BOX:
        return LEFT_BOX + RIGHT_BOX
    if ch == EMPTY:
        return EMPTY + EMPTY
    return BOT + EMPTY

def parse_wide(filename):
    grid = []
    moves = ''
    start = (0, 0)
    with open(filename, 'r') as file:
        lines = file.read()
        start, actions = lines.strip().split('\n\n')
        board = start.split('\n')
        for r in range(len(board)):
            grid.append([])
            for c in range(len(board[r])):
                grid[-1].extend(widen(board[r][c]))
                if board[r][c] == BOT:
                    start = (r, c * 2)
        moves = ''.join(actions.split('\n'))
    return grid, moves, start

def pprint_grid(grid):
    for r in grid:
        s = ''
        for c in r:
            s += c
        print(s)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    grid, moves, start = parse(filename)
    grid = simulate(grid, moves, start)
    print(calc_gps(grid))

    grid, moves, start = parse_wide(filename)
    grid = simulate_wide(grid, moves, start)
    print(calc_gps(grid, LEFT_BOX))