import re
from collections import deque

BLUEPRINT_PARSE = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\.")


def tri(n):
    return (n * (n + 1)) // 2


def sum_tuples(*tuples):
    return tuple(map(lambda *args: sum(args), *tuples))


# offset triangles so time[1] returns 0, time [2] returns 1, etc
TRIANGLE_NUMBERS = [tri(t - 1) for t in range(33)]


def parse(filename):
    blueprints = []
    with open(filename, 'r') as file:
        for line in file:
            result = re.match(BLUEPRINT_PARSE, line)
            blueprint = (int(result[1]), {0: int(result[2])}, {0: int(result[3])}, {0: int(result[4]), 1: int(result[5])}, {0: int(result[6]), 2: int(result[7])})
            blueprints.append(blueprint)
    return blueprints


def print_blueprint(blueprint):
    print(
        f"Blueprint {blueprint[0]}: Each ore robot costs {blueprint[1]} ore. Each clay robot costs {blueprint[2]} ore. Each obsidian robot costs {blueprint[3][0]} ore and {blueprint[3][1]} clay. Each geode robot costs {blueprint[4][0]} ore and {blueprint[4][2]} obsidian.")


def determine_blueprint_quality(minutes, blueprint, starting_bots, starting_mats, max_bots):
    # key is (minutes remaining, (quantity of bots), (quantity of mats))
    # value is the best value for that subproblem
    memo = dict()
    return determine_quality(minutes, blueprint, starting_bots, starting_mats, max_bots, memo, 0)


def can_build(mats, bot_blueprint):
    for mat_type in bot_blueprint:
        if mats[mat_type] < bot_blueprint[mat_type]:
            return False

    return True


def chuck_extra_mats(mats, max_bots, moves_left, bots):
    # don't chuck geodes
    for idx in range(0, len(mats) - 1):
        mats[idx] = min(mats[idx], max_bots[idx] * moves_left - (bots[idx] * moves_left - 1))


def determine_quality(moves_left, blueprint, bot_qty, mats_qty, max_bots, memo, best_so_far):

    if mats_qty[3] + bot_qty[3] * moves_left + TRIANGLE_NUMBERS[moves_left] <= best_so_far:
        return 0

    chuck_extra_mats(mats_qty, max_bots, moves_left, bot_qty)
    key = (moves_left, tuple(bot_qty), tuple(mats_qty))

    if moves_left <= 0:
        return mats_qty[3]

    quality = -1

    # for each bot we can build
    for bot_to_build in range(0, len(bot_qty)):
        if bot_qty[bot_to_build] >= max_bots[bot_to_build] and not bot_to_build == len(bot_qty) - 1:
            # building this bot gives us nothing
            continue

        new_moves = moves_left
        new_bots = bot_qty.copy()
        new_mats = mats_qty.copy()
        bot_blueprint = blueprint[bot_to_build + 1]

        # can't build a bot that requires clay if we don't have a clay bot
        if 1 in bot_blueprint and new_bots[1] == 0:
            continue

        # can't build a bot that requries obsidian if we don't have an obsidian bot
        if 2 in bot_blueprint and new_bots[2] == 0:
            continue

        # wait until we can build the bot...
        while not can_build(new_mats, bot_blueprint) and new_moves > 1:
            new_moves -= 1
            for bot_type in range(0, len(new_bots)):
                new_mats[bot_type] += new_bots[bot_type]

        building = can_build(new_mats, bot_blueprint)

        # if we can, spend mats
        if building:
            for mat_type in bot_blueprint:
                new_mats[mat_type] -= bot_blueprint[mat_type]

        # gather mats:
        for bot_type in range(0, len(new_bots)):
            new_mats[bot_type] += new_bots[bot_type]

        # add the new bot to our inventory if we built it
        if building:
            new_bots[bot_to_build] += 1

        # recurse
        choice_quality = determine_quality(new_moves - 1, blueprint, new_bots, new_mats, max_bots, memo, quality)
        quality = max(choice_quality, quality)

    # memo[key] = quality
    return quality


def determine_max_bots(blueprint):
    # need to determine the max value for each material type
    max_mats = []
    for mat in range(0, 4):
        max_mat = 0
        for bot in range(0, 4):
            if mat in blueprint[bot + 1]:
                max_mat = max(max_mat, blueprint[bot + 1][mat])
        max_mats.append(max_mat)
    return max_mats


def limit_bots(bots, max_bots):
    limit = []
    for idx in range(len(bots) - 1):
        limit.append(min(bots[idx], max_bots[idx]))
    limit.append(bots[-1])
    return tuple(limit)


def limit_mats(mats, bots, max_bots, time):
    limit = []
    for idx in range(len(mats) - 1):
        limit.append(min(mats[idx], (time * max_bots[idx]) - (bots[idx] * (time - 1))))
    limit.append(mats[-1])
    return tuple(limit)


def bfs(moves, blueprint, starting_bots, max_bots):
    memo = set()
    best = 0
    q = deque()

    # q stores tuple of (time left, bots, mats, set of bots that can't be built because we skipped them previously)
    start = (moves, starting_bots, (0, 0, 0, 0), set())
    q.append(start)

    while len(q) > 0:
        time, bots, mats, cant_build = q.popleft()
        best = max(best, mats[3])

        # no time remaining
        if time == 0:
            continue

        # We're not building any robots anymore, no point in continuing this branch
        if len(cant_build) == 4:
            continue

        bots = limit_bots(bots, max_bots)
        mats = limit_mats(mats, bots, max_bots, time)

        cur_state = (time, bots, mats)

        # already been here, no need to do it again
        if cur_state in memo:
            continue

        memo.add(cur_state)

        # can't beat current best with most optimistic geode gathering
        if mats[3] + bots[3] * time + TRIANGLE_NUMBERS[time] <= best:
            continue

        buildable = [mats[0] >= blueprint[1][0], mats[0] >= blueprint[2][0], mats[0] >= blueprint[3][0] and mats[1] >= blueprint[3][1], mats[0] >= blueprint[4][0] and mats[2] >= blueprint[4][2]]
        skipped_building = set([idx for idx in range(len(buildable)) if buildable[idx]])
        skipped_building.update(cant_build)

        new_mats = sum_tuples(bots, mats)
        q.append((time - 1, bots, new_mats, skipped_building))

        if buildable[0] and 0 not in cant_build:
            q.append((time - 1, sum_tuples(bots, (1, 0, 0, 0)), sum_tuples(new_mats, (-1 * blueprint[1][0], 0, 0, 0)), set()))

        if buildable[1] and 1 not in cant_build:
            q.append((time - 1, sum_tuples(bots, (0, 1, 0, 0)), sum_tuples(new_mats, (-1 * blueprint[2][0], 0, 0, 0)), set()))

        if (buildable[2]) and 2 not in cant_build:
            q.append((time - 1, sum_tuples(bots, (0, 0, 1, 0)), sum_tuples(new_mats, (-1 * blueprint[3][0], -1 * blueprint[3][1], 0, 0)), set()))

        if (buildable[3]) and 3 not in cant_build:
            q.append((time - 1, sum_tuples(bots, (0, 0, 0, 1)), sum_tuples(new_mats, (-1 * blueprint[4][0], 0, -1 * blueprint[4][2], 0)), set()))

    return best


def pt1(blueprints):
    qualities = []
    for blueprint in blueprints:
        print(blueprint[0])
        max_bots = determine_max_bots(blueprint)
        quality = determine_blueprint_quality(24, blueprint, [1, 0, 0, 0], [0, 0, 0, 0], max_bots) * blueprint[0]
        qualities.append(quality)
    return sum(qualities)


def pt2(blueprints):
    total = 1
    for idx in range(0, min(len(blueprints), 3)):
        blueprint = blueprints[idx]
        print(blueprint[0])
        max_bots = determine_max_bots(blueprint)
        # geodes = determine_blueprint_quality(32, blueprint, [1, 0, 0, 0], [0, 0, 0, 0], max_bots)
        geodes = bfs(32, blueprint, (1, 0, 0, 0), max_bots)
        total *= geodes
    return total


def main():
    test = False
    filename = "./s/input.txt"

    if test:
        filename = "./s/test.txt"

    blueprints = parse(filename)
    print(pt1(blueprints))
    print(pt2(blueprints))


if __name__ == "__main__":
    main()
