def parse_line(line):
    return [[int(a) for a in split.split("-")] for split in line.split(",")]

def order(a, b):
    if b[0] < a[0]:
        return [b, a]
    return [a, b]

def contains(a, b):
    return a[1] >= b[1] or a[0] == b[0]

def overlap(a, b):
    return a[1] >= b[0] or a[0] == b[0]

test = False
filename = "input.txt"

if test:
    filename = "test.txt"

pt1 = 0
pt2 = 0
with open(filename, 'r') as infile:
    for line in infile.readlines():
        ranges = parse_line(line.strip())
        ranges = order(ranges[0], ranges[1])
        if contains(ranges[0], ranges[1]):
            pt1 = pt1 + 1
        if overlap(ranges[0], ranges[1]):
            pt2 = pt2 + 1

print("Part 1:", pt1)
print("Part 2:", pt2)
