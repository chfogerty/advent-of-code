from pprint import pprint

def is_in_range(forest, x, y):
    if x < 0 or y < 0:
        return False
    if x > len(forest) or y > len(forest[0]):
        return False
    return True

def can_see_up(forest, vis, x, y):
    seen = 0
    for i in range(x + 1, len(forest)):
        seen += 1
        if forest[i][y] >= forest[x][y]:
            # tree is blocked
            return (False, seen)

        # if forest[i][y] < forest[x][y] and vis[i][y]:
        #     # shortcut if we've already calculated to this point
        #     return (True, seen)

    # in case none of the other shortcuts work
    return (True, seen)

def can_see_down(forest, vis, x, y):
    seen = 0
    for i in range(x - 1, -1, -1):
        seen += 1
        if forest[i][y] >= forest[x][y]:
            return (False, seen)
        
        # if forest[i][y] < forest[x][y] and vis[i][y]:
        #     return (True, seen)
    
    return (True, seen)

def can_see_left(forest, vis, x, y):
    seen = 0
    for i in range(y - 1, -1, -1):
        seen += 1
        if forest[x][i] >= forest[x][y]:
            return (False, seen)
        
        # if forest[x][i] < forest[x][y] and vis[x][i]:
        #     return (True, seen)
        
    return (True, seen)

def can_see_right(forest, vis, x, y):
    seen = 0
    for i in range(y + 1, len(forest[x])):
        seen += 1
        if forest[x][i] >= forest[x][y]:
            return (False, seen)
        
        # if forest[x][i] < forest[x][y] and vis[x][i]:
        #     return (True, seen)

    return (True, seen)

test = False
filename = "./h/input.txt"

if test:
    filename = "./h/test.txt"

forest = []

with open(filename, 'r') as file:
    for line in file:
        forest.append([])
        l = line.strip()
        for c in l:
            forest[-1].append(int(c))

vis = [[False for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
vis_u = [[False for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
vis_d = [[False for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
vis_l = [[False for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
vis_r = [[False for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]

scenic = [[0 for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
scenic_u = [[0 for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
scenic_d = [[0 for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
scenic_l = [[0 for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]
scenic_r = [[0 for _ in range(0, len(forest[i]))] for i in range(0, len(forest))]

for x in range(0, len(forest)):
    for y in range(0, len(forest[x])):
        d = can_see_down(forest, vis_d, x, y)
        l = can_see_left(forest, vis_l, x, y)
        vis_d[x][y] = d[0]
        vis_l[x][y] = l[0]
        scenic_d[x][y] = d[1]
        scenic_l[x][y] = l[1]

count = 0
best = 0
for x in range(len(forest) - 1, -1, -1):
    for y in range(len(forest[x]) - 1, -1, -1):
        u = can_see_up(forest, vis_u, x, y)
        r = can_see_right(forest, vis_r, x, y)
        vis_u[x][y] = u[0]
        vis_r[x][y] = r[0]
        scenic_u[x][y] = u[1]
        scenic_r[x][y] = r[1]
        vis[x][y] = vis_u[x][y] or vis_d[x][y] or vis_l[x][y] or vis_r[x][y]
        if vis[x][y]:
            count += 1
        scenic[x][y] = scenic_d[x][y] * scenic_l[x][y] * scenic_r[x][y] * scenic_u[x][y]
        if scenic[x][y] > best:
            best = scenic[x][y]

print(count)
print(best)