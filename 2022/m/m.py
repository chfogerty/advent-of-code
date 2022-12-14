from enum import Enum
from functools import cmp_to_key

FIRST_DIVIDER = [[2]]
SECOND_DIVIDER = [[6]]


def compare_int(left, right):
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def compare_list(left, right):
    for idx in range(0, min(len(left), len(right))):
        result = compare_packets(left[idx], right[idx])
        if result != 0:
            return result
    return compare_int(len(left), len(right))


def compare_packets(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return compare_int(left, right)
    if isinstance(left, list) and isinstance(right, list):
        return compare_list(left, right)
    if isinstance(left, list):
        return compare_list(left, [right])
    if isinstance(right, list):
        return compare_list([left], right)


def parse_file(filename):
    data = []
    with open(filename, 'r') as file:
        for rawline in file:
            line = rawline.strip()
            if len(line) == 0:
                continue

            data.append(eval(line))
    return data


def decoder_key(packets):
    first_loc = 0

    for idx in range(0, len(packets)):
        if packets[idx] == FIRST_DIVIDER:
            first_loc = idx + 1
        elif packets[idx] == SECOND_DIVIDER:
            return first_loc * (idx + 1)


def run_comparison(packets):
    total = 0
    for idx in range(0, len(packets), 2):
        result = compare_packets(packets[idx], packets[idx+1])
        if result == -1:
            total += (idx // 2) + 1
    return total


def main():
    test = False
    filename = "./m/input.txt"

    if test:
        filename = "./m/test.txt"

    packets = parse_file(filename)
    print(run_comparison(packets))
    packets.append(FIRST_DIVIDER)
    packets.append(SECOND_DIVIDER)
    sorted_packets = sorted(packets, key=cmp_to_key(compare_packets))
    print(decoder_key(sorted_packets))


if __name__ == "__main__":
    main()
