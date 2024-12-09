def rle_checksum(rl_disk):
    chksum = 0
    idx = 0
    for data in rl_disk:
        for _ in range(data[1]):
            chksum += idx * max(data[0], 0)
            idx += 1
    return chksum

def checksum(disk):
    chksum = 0
    idx = 0
    while disk[idx] != -1:
        chksum += idx * disk[idx]
        idx += 1
    return chksum

# maybe unused
# def find_free_space(rl_disk):
#     # returns dict
#     #   key: size
#     #   val: array of space idx sorted small to large
#     free_space = dict()
#     max_size = -1
#     for idx in range(len(rl_disk)):
#         if rl_disk[idx][0] == -1:
#             size = rl_disk[idx][1]
#             if size not in free_space.keys():
#                 free_space[size] = []
#             free_space[size].append(idx)
#             if size > max_size:
#                 max_size = size
#     return free_space, max_size

def find_free_space(rl_disk, min_size):
    for idx in range(len(rl_disk)):
        data = rl_disk[idx]
        if data[0] == -1 and data[1] >= min_size:
            return idx
    return -1

def rle_compact(rl_disk):
    rptr = len(rl_disk) - 1
    compacted = rl_disk.copy()

    while rptr > 0:
        if compacted[rptr][0] == -1:
            rptr -= 1
            continue
        free_space = find_free_space(compacted[:rptr], compacted[rptr][1])
        if free_space == -1:
            # none found
            rptr -= 1
            continue
        # update free space at new location
        compacted[free_space] = (-1, compacted[free_space][1] - compacted[rptr][1])
        # add file to location
        compacted.insert(free_space, compacted[rptr])
        rptr += 1
        # remove old file
        compacted[rptr] = (-1, compacted[rptr][1])
    return compacted


def compact(disk):
    rptr = len(disk) - 1
    lptr = 0
    compacted = disk.copy()

    while lptr < rptr:
        if compacted[rptr] == -1:
            rptr -= 1
            continue
        if compacted[lptr] != -1:
            lptr += 1
            continue

        if compacted[lptr] == -1:
            compacted[lptr] = compacted[rptr]
            compacted[rptr] = -1
            rptr -= 1
            lptr += 1
    return compacted

def rle_disk(disk):
    # tuple of (file, length)
    # file is the id, or -1 for free space
    rl_disk = []
    idx = 0
    while idx < len(disk):
        data = disk[idx]
        count = 0
        while idx < len(disk) and disk[idx] == data:
            count += 1
            idx += 1
        rl_disk.append((data, count))
    return rl_disk

def parse(filename):
    disk = []

    with open(filename, 'r') as file:
        blocks = [int(x) for x in file.readline().strip()]
        for idx in range(len(blocks)):
            for _ in range(blocks[idx]):
                data = -1 if idx % 2 == 1 else idx // 2
                disk.append(data)

    return disk

def pprint_disk(disk):
    s = ''
    for data in disk:
        s += '.' if data == -1 else f'{data}'
    print(s)

def pprint_rl_disk(rl_disk):
    s = ''
    for data in rl_disk:
        for _ in range(data[1]):
            s += '.' if data[0] == -1 else f'{data[0]}'
    print(s)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    disk = parse(filename)
    compacted = compact(disk)
    print(checksum(compacted))

    rl_disk = rle_disk(disk)
    rl_compacted = rle_compact(rl_disk)
    print(rle_checksum(rl_compacted))