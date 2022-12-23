from collections import deque


def parse(filename, key=1):
    dq = deque()
    l = []
    with open(filename, 'r') as file:
        for line in file:
            val = int(line)*key
            l.append(val)
            dq.append((val, len(l) - 1))

    return dq, l


def rotate_to_start(dq, item):
    idx = dq.index(item)
    if idx < len(dq) / 2:
        dq.rotate(-1*idx)
    else:
        dq.rotate(len(dq) - idx)


def mix(dq, initial_order):
    zero_idx = None
    for idx in range(0, len(initial_order)):
        val_to_find = initial_order[idx]
        rotate_to_start(dq, (val_to_find, idx))
        dq_item = dq.popleft()
        if dq_item[0] == 0:
            zero_idx = dq_item[1]
        else:
            sign = int(dq_item[0] / abs(dq_item[0]))
            rotation = sign * (abs(dq_item[0]) % len(dq))
            if abs(rotation) < len(dq) / 2:
                rotation *= -1
            else:
                rotation = sign * (len(dq) - abs(rotation))
            dq.rotate(rotation)
        dq.appendleft(dq_item)

    rotate_to_start(dq, (0, zero_idx))


def decode(dq):
    first_idx = 1000 % len(dq)
    second_idx = 2000 % len(dq)
    third_idx = 3000 % len(dq)
    l = list(dq)
    return l[first_idx][0] + l[second_idx][0] + l[third_idx][0]


def print_deque(dq):
    s = ""
    for item in dq:
        s += f"{item[0]}, "
    print(s[:-2])


def main():
    test = False
    filename = "./t/input.txt"

    if test:
        filename = "./t/test.txt"

    dq, l = parse(filename, key=811589153)
    for _ in range(0, 10):
        mix(dq, l)
    print(decode(dq))


if __name__ == "__main__":
    main()
