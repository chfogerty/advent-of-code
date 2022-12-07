from itertools import zip_longest

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def get_compartments(rucksack):
    middle = len(rucksack)//2
    left = {item for item in rucksack[:middle]}
    right = {item for item in rucksack[middle:]}
    
    compartments = (left, right)
    return compartments

def common_item(compartments):
    return compartments[0].intersection(compartments[1]).pop()

def priority(item):
    return alphabet.find(item) + 1

test = False
total = 0
filename = 'input.txt'

if test:
    filename = 'test.txt'

#part 1
with open(filename, 'r') as infile:
    for line in infile.readlines():
        total = total + priority(common_item(get_compartments(line.strip())))

print("Part 1:", total)

#part 2
pt2_total = 0
with open(filename, 'r') as infile:
    groups = list(zip_longest(*(iter([line.strip() for line in infile.readlines()]),) *3))
    for group in groups:
        group_set = [{item for item in group[x]} for x in range(0, len(group))]
        first = group_set[0].intersection(group_set[1])
        second = first.intersection(group_set[2])
        pt2_total = pt2_total + priority(second.pop())

print("Part 2:", pt2_total)


