import re


def extract_values(filename):
    values = [0, 1]
    cycle = 1
    x = 1
    adding = False
    adding_value = 0
    with open(filename, 'r') as file:
        line = file.readline()
        while line != '':
            if adding:
                x += adding_value
                adding = False
                line = file.readline()
            else:
                if "addx" in line:
                    result = re.match(VALUE, line.strip())
                    adding = True
                    adding_value = int(result[1])
                else:
                    line = file.readline()

            cycle += 1
            values.append(x)
    return values


def find_signal(values):
    s = 0
    for i in range(20, 221, 40):
        s += i * values[i]
    return s


def get_pixel_span(loc):
    return [loc - 1, loc, loc + 1]


def construct_message(values):
    screen = []
    for row in range(0, 6):
        screen.append([])
        for pixel in range(0, 40):
            cycle = row * 40 + pixel + 1
            loc = values[cycle]
            span = get_pixel_span(loc)
            if pixel in span:
                screen[-1].append('#')
            else:
                screen[-1].append(' ')
    return screen


def print_message(screen):
    for row in screen:
        print(''.join(row))


def main():
    test = False
    filename = "./j/input.txt"

    if test:
        filename = "./j/test.txt"

    values = extract_values(filename)
    print(find_signal(values))
    print_message(construct_message(values))


VALUE = re.compile(".* (-?[0-9]+)")

if __name__ == "__main__":
    main()
