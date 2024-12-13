import re

NUMBERS = re.compile(r'.*X[+=](\d+), Y[+=](\d+)')
A = "A"
B = "B"
PRIZE = "PRIZE"
CYCLE = [A, B, PRIZE]

def invert_matrix(matrix):
    determinant = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    a = matrix[0][0]
    b = matrix[0][1]
    c = matrix[1][0]
    d = matrix[1][1]
    inverse = [[d, -1*b], [-1*c, a]]
    return (determinant, inverse)

def multiply_matrix(a, b):
    result = []
    determinant, inverse_a = invert_matrix(a)
    for row in inverse_a:
        total = 0
        for c in range(len(row)):
            total += row[c] * b[c][0]
        result.append(total / determinant)
    return result

def calculate_tokens(games):
    total = 0
    for game in games:
        a_press, b_press = multiply_matrix(game[0], game[1])
        if int(a_press) == a_press and int(b_press) == b_press:
            total += int(a_press) * 3 + int(b_press)
    return total



def process_raw_games(raw_games, offset=0):
    # matrix in the format
    # AX AY
    # BX BY
    # followed by matrix in the format
    # PRIZEX
    # PRIZEY
    games = []
    for game in raw_games:
        coeff = [[game[A][0], game[B][0]], [game[A][1], game[B][1]]]
        const = [[game[PRIZE][0] + offset], [game[PRIZE][1] + offset]]
        games.append((coeff, const))
    return games

def parse(filename, offset=0):
    raw_games = []
    line_count = 0
    with open(filename, 'r') as file:
        for line in file:
            numbers = NUMBERS.match(line)
            if numbers:
                pair = (int(numbers[1]), int(numbers[2]))
                if line_count % 4 == 0:
                    raw_games.append(dict())
                raw_games[-1][CYCLE[line_count % 4]] = pair
            line_count += 1
    return process_raw_games(raw_games, offset)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    games = parse(filename)
    print(calculate_tokens(games))

    games = parse(filename, offset=10000000000000)
    print(calculate_tokens(games))