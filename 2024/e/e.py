# does this sort backward? Yes
# does it matter? Nope
def sort(update, dependencies):
    sorted = update.copy()
    for i in range(len(sorted)-1, 0, -1):
        j = 0
        while j < i:
            left = sorted[j]
            right = sorted[j+1]
            if right in dependencies.keys() and left in dependencies[right]:
                sorted[j] = right
                sorted[j+1] = left
            j += 1
    return sorted



def get_middle_page(update):
    return update[len(update) // 2]

def in_order(update, dependencies):
    for i in range(0, len(update)-1):
        if update[i] in dependencies.keys():
            for page in update[i+1:]:
                if page in dependencies[update[i]]:
                    return False
    return True

def parse(filename):
    dependencies = dict()
    updates = []
    with open(filename, 'r') as file:
        # dependencies
        while True:
            line = file.readline()
            if line.rstrip() == "":
                break

            pages = [int(x) for x in line.rstrip().split('|')]
            if pages[1] not in dependencies.keys():
                dependencies[pages[1]] = set()
            dependencies[pages[1]].add(pages[0])

        while True:
            line = file.readline()
            if not line:
                break

            updates.append([int(x) for x in line.rstrip().split(',')])

    return (dependencies, updates)


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    dependencies, updates = parse(filename)

    p1_total = 0
    p2_total = 0
    for update in updates:
        if in_order(update, dependencies):
            p1_total += get_middle_page(update)
        else:
            sorted = sort(update, dependencies)
            p2_total += get_middle_page(sorted)
            
    print(p1_total)
    print(p2_total)