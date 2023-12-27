NUMBERS = "0123456789"
def parse(filename):
    board = []
    symbols = []
    with open(filename, 'r') as file:
        row = 0
        for rawline in file:
            col = 0
            board.append([c for c in rawline.strip()])
            for c in rawline.strip():
                if not(c in NUMBERS) and not(c == '.'):
                    symbols.append((c, (row, col)))
                col += 1
            row += 1
    return (board, symbols)

def get_adjacent(loc, max_row, max_col):
    adjacent = []
    for row in range (loc[0] - 1, loc[0] + 2, 1):
        for col in range (loc[1] - 1, loc[1] + 2, 1):
            if row < 0 or col < 0 or col > max_col or row > max_row or (row == loc[0] and col == loc[1]):
                pass
            else:
                adjacent.append((row, col))
    return adjacent

# return (number, (row, (col start, col end)))
def find_number(known, board):
    row, start_col = known
    end_col = start_col
    while start_col >= 0 and board[row][start_col] in NUMBERS:
        start_col -= 1
    
    while end_col < (len(board[0]) - 1) and board[row][end_col] in NUMBERS:
        end_col += 1

    # we went past the number, we want the range to be [start, end)
    start_col += 1
    number = 0
    for col in range(start_col, end_col, 1):
        number *= 10
        number += NUMBERS.find(board[row][col])
    return (number, (row, (start_col, end_col)))

def part_1(board, symbols):
    total = 0
    # set is (row, (col start, col end))
    counted_numbers = set()
    for _, loc in symbols:
        adjacent_spots = get_adjacent(loc, len(board), len(board[0]))
        for row, col in adjacent_spots:
            if board[row][col] in NUMBERS:
                number, position = find_number((row, col), board)
                if position not in counted_numbers:
                    counted_numbers.add(position)
                    total += number

    return total

def part_2(board, symbols):
    total = 0
    for symbol, loc in symbols:
        if symbol == '*':
            cur_total = 1
            counted_numbers = set()
            adjacent = get_adjacent(loc, len(board), len(board[0]))
            for row, col in adjacent:
                if board[row][col] in NUMBERS:
                    number, position = find_number((row, col), board)
                    if position not in counted_numbers:
                        counted_numbers.add(position)
                        cur_total *= number
            if len(counted_numbers) == 2:
                total += cur_total
    return total

def main():
    test = False
    filename = "./c/input.txt"

    if test:
        filename = "./c/test.txt"
    
    board, symbols = parse(filename)
    print(part_1(board, symbols))
    print(part_2(board, symbols))


if __name__ == "__main__":
    main()