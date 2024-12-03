import re

MULTIPLY = re.compile(r"mul\((\d+),(\d+)\)")
ALL = re.compile(r"((?:mul\(\d+,\d+\))|(?:don't\(\))|(?:do\(\)))")

def parse(filename, regex):
    matches = []
    with open(filename, 'r') as file:
        for line in file:
            matches.extend(regex.findall(line))
    return matches

def pt1(matches):
    values = [int(m[0]) * int(m[1]) for m in matches]
    print(sum(values))

def pt2(matches):
    total = 0
    enabled = True
    for match in matches:
        if match[0] == 'm' and enabled:
            groups = MULTIPLY.match(match).groups()
            total += int(groups[0]) * int(groups[1])
        if match == "don't()":
            enabled = False
        if match == "do()":
            enabled = True
    print(total)


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    p1_matches = parse(filename, MULTIPLY)
    pt1(p1_matches)

    p2_matches = parse(filename, ALL)
    pt2(p2_matches)