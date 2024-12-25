def fits(key, lock):
    for i in range(len(key)):
        if key[i] + lock[i] > 5:
            return False
    return True

def parse(filename):
    keys = dict()
    locks = []
    with open(filename, 'r') as file:
        lines = file.read()
        objects = lines.strip().split('\n\n')
        for obj in objects:
            lock = [0]*5
            key = [5]*5
            rows = obj.strip().split('\n')
            for idx in range(1, len(rows)-1):
                row = rows[idx]
                for c_idx in range(len(row)):
                    if row[c_idx] == '#':
                        lock[c_idx] += 1
                    else:
                        key[c_idx] -= 1
            if obj[0] == '#':
                locks.append(lock)
            else:
                key_total = sum(key)
                if key_total not in keys:
                    keys[key_total] = []
                keys[key_total].append(key)
    return locks, keys

def find_matching(locks, keys):
    matches = 0
    for lock in locks:
        l_tot = sum(lock)
        k_tot_max = 25 - l_tot
        for k_tot in range(k_tot_max, 0, -1):
            if k_tot not in keys:
                continue
            for key in keys[k_tot]:
                if fits(key, lock):
                    matches += 1
    return matches

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    locks, keys = parse(filename)
    print(find_matching(locks, keys))