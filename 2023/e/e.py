def parse(filename):
    seeds = []
    maps = []
    idx = -1
    with open(filename, 'r') as file:
        for rawline in file:
            line = rawline.strip()
            if line == '':
                maps.append([])
                idx += 1
            elif idx == -1 or not(line[0].isalpha()):
                if idx == -1:
                    seeds.extend([int(n) for n in line.split(' ')[1:]])
                else:
                    maps[idx].append([int(n) for n in line.split(' ')])
    return (seeds, maps)

def part_1(seeds, maps):
    lowest = -1
    for seed in seeds:
        current = seed
        for map_kind in maps:
            used = False
            for range_map in map_kind:
                src_start = range_map[1]
                src_end = range_map[1] + range_map[2]
                if not(used) and current in range(src_start, src_end):
                    current = current + (range_map[0] - range_map[1])
                    used = True
        if lowest == -1 or current < lowest:
            lowest = current
    return lowest

def part_2(seed_ranges, maps):
    seeds = []
    for idx in range(0, len(seed_ranges), 2):
        start = seed_ranges[idx]
        end = seed_ranges[idx] + seed_ranges[idx+1]
        seeds.extend(range(start, end))
    return part_1(seeds, maps)

def main():
    test = False
    filename = "./e/input.txt"

    if test:
        filename = "./e/test.txt"

    seeds, maps = parse(filename)
    print(part_1(seeds, maps))
    print(part_2(seeds, maps))


if __name__ == "__main__":
    main()