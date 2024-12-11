def p2_blink(stones, iterations):
    memo = dict()
    total = 0
    for stone in stones:
        total += memo_blink(stone, iterations, memo)
    return total

def memo_blink(stone, iterations, memo):
    if iterations == 0:
        return 1
    elif (stone, iterations) in memo:
        return memo[(stone, iterations)]
    else:
        total = 0
        for next in blink(stone):
            total += memo_blink(next, iterations - 1, memo)
        memo[(stone, iterations)] = total
        return total

def p1_blink(stones):
    new_stones = []
    for stone in stones:
        new_stones.extend(blink(stone))
    return new_stones

def blink(stone):
    if stone == 0:
        return [1]
    elif len(f'{stone}') % 2 == 0:
        stone_str = f'{stone}'
        new_len = len(stone_str) // 2
        return [int(stone_str[:new_len]), int(stone_str[new_len:])]
    else:
        return [stone * 2024]

def parse(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        return [int(stone) for stone in line.split()]

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    stones = parse(filename)

    # This is what I actually did for p1. Couldn't
    # keep it for p2 because it modified stones
    # for idx in range(25):
    #     stones = p1_blink(stones)
    # print(len(stones))

    print(p2_blink(stones, 25))
    print(p2_blink(stones, 75))