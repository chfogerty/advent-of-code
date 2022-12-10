import re


class Knot:
    def __init__(self):
        self.history = [(0, 0)]

    def set_position(self, x, y):
        self.history.append((x, y))

    def get_position(self):
        return self.history[-1]

    def move_up(self):
        self.move(0, 1)

    def move_down(self):
        self.move(0, -1)

    def move_right(self):
        self.move(1, 0)

    def move_left(self):
        self.move(-1, 0)

    def move(self, dx, dy):
        cur = self.history[-1]
        self.history.append((cur[0] + dx, cur[1] + dy))

    def distance(self, other):
        this_cur = self.get_position()
        other_cur = other.get_position()
        return abs(this_cur[0] - other_cur[0]) + abs(this_cur[1] - other_cur[1])

    def move_toward(self, other):
        this_cur = self.get_position()
        other_cur = other.get_position()
        dx = other_cur[0] - this_cur[0]
        dy = other_cur[1] - this_cur[1]

        if abs(dx) < 2 and abs(dy) < 2:
            self.move(0, 0)
            return

        move_x = 0
        move_y = 0

        if abs(dx) > 0:
            move_x = dx // abs(dx)

        if abs(dy) > 0:
            move_y = dy // abs(dy)

        self.move(move_x, move_y)

    def __str__(self):
        return f"({self.history[-1][0]}, {self.history[-1][1]})"


def simulate_knots(filename, count):
    knots = [Knot() for _ in range(0, count)]
    with open(filename, 'r') as file:
        for line in file:
            result = re.match(LINE, line.strip())
            repeat = int(result[2])
            for _ in range(0, repeat):
                if result[1] == 'U':
                    knots[0].move_up()
                elif result[1] == 'D':
                    knots[0].move_down()
                elif result[1] == 'L':
                    knots[0].move_left()
                elif result[1] == 'R':
                    knots[0].move_right()

                for i in range(1, len(knots)):
                    knots[i].move_toward(knots[i-1])
    return len(set(knots[-1].history))


def main():
    test = False
    filename = "./i/input.txt"

    if test:
        filename = "./i/test.txt"

    print(simulate_knots(filename, 2))
    print(simulate_knots(filename, 10))


LINE = re.compile("([UDLR]) ([0-9]+)")

if __name__ == "__main__":
    main()
