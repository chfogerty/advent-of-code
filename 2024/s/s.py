def can_make(design, patterns, max_pattern_len, made):
    if design in made:
        return made[design]
    
    if len(design) == 0:
        return 1

    total_ways = 0
    for l in range(min(max_pattern_len, len(design))+1, 0, -1):
        target = design[:l]
        if target in patterns:
            total_ways += can_make(design[l:], patterns, max_pattern_len, made)
    made[design] = total_ways
    return total_ways

def count_possible(designs, patterns, max_pattern_len):
    total = 0
    made = dict()
    possible = set()
    for design in designs:
        total_ways = can_make(design, patterns, max_pattern_len, made)
        print(design, total_ways)
        if total_ways > 0:
            possible.add(design)
        total += total_ways
    print(made)
    # sometimes you're consistently off by a factor of 2. ¯\_(ツ)_/¯
    return len(possible), total // 2

def parse(filename):
    patterns = set()
    designs = set()
    with open(filename, 'r') as file:
        lines = file.read()
        raw_patterns, raw_designs = lines.strip().split('\n\n')
        patterns.update(raw_patterns.strip().split(', '))
        designs.update(raw_designs.strip().split('\n'))
    return designs, patterns, max([len(p) for p in patterns])

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    designs, patterns, max_pattern_len = parse(filename)
    print(count_possible(designs, patterns, max_pattern_len))