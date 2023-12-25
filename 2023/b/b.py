import re

RED = 0
GRE = 1
BLU = 2

FIND_RED = re.compile("(\d+) red")
FIND_BLUE = re.compile("(\d+) blue")
FIND_GREEN = re.compile("(\d+) green")

def get_count(pull, regex):
    res = regex.findall(pull)
    if res is None or len(res) == 0:
        return 0
    return int(res[0])

def parse(filename):
    games = []
    with open(filename, 'r') as file:
        for rawline in file:
            rawgames = rawline.split(':')[1].strip()
            pulls = rawgames.split(';')
            max_red = 0
            max_green = 0
            max_blue = 0
            for pull in pulls:
                red = get_count(pull, FIND_RED)
                max_red = max(red, max_red)
                green = get_count(pull, FIND_GREEN)
                max_green = max(green, max_green)
                blue = get_count(pull, FIND_BLUE)
                max_blue = max(blue, max_blue)
            games.append((max_red, max_green, max_blue))
    return games

def part_1(games):
    MAX_CUBES = (12, 13, 14)
    total = 0
    idx = 1
    for game in games:
        if game[0] <= MAX_CUBES[0] and game[1] <= MAX_CUBES[1] and game[2] <= MAX_CUBES[2]:
            total += idx
        idx += 1
    return total

def part_2(games):
    total = 0
    for game in games:
        total += (game[0] * game[1] * game[2])
    return total

def main():
    test = False
    filename = "./b/input.txt"

    if test:
        filename = "./b/test.txt"
    
    games = parse(filename)
    print(part_1(games))
    print(part_2(games))


if __name__ == "__main__":
    main()
