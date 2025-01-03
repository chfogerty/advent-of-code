move_points = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}

# 3 beats 2 beats 1 beats 3
def match_score(them, me):
    if them == me:
        return (3, 3)
    if them == 1 and me == 3:
        return (6, 0)
    if them == 3 and me == 1:
        return (0, 6)
    if them > me:
        return (6, 0)
    if them < me:
        return (0, 6)

def run_strategy_pt1(matches):
    my_score = 0
    for match in matches:
        their_move = move_points[match[0]]
        my_move = move_points[match[1]]
        my_score = my_score + my_move + match_score(their_move, my_move)[1]
    print(my_score)

def calc_move(their_move, adjustment):
    my_move = their_move + adjustment

    if my_move == 0:
        my_move = 3
    elif my_move == 4:
        my_move = 1
    return my_move

# X is lose (-1), Y is draw (0), Z is win (+1)
def run_strategy_pt2(matches):
    my_score = 0
    for match in matches:
        their_move = move_points[match[0]]
        adjustment = move_points[match[1]] - 2
        my_move = calc_move(their_move, adjustment)
        my_score = my_score + my_move + match_score(their_move, my_move)[1]
    print(my_score)
        


test = [['A', 'Y'], ['B', 'X'], ['C', 'Z']]
run_strategy_pt1(test)        
run_strategy_pt2(test)

strats = """B Y
A Z
C Z
A Y
A Y
B Y
C Y
A Y
B Y
B Y
A Y
B Z
B Y
A Y
C Y
B X
B Y
B Y
B Y
C Y
B Y
A Y
B Y
A Y
B Y
C Y
A Y
B X
B Y
B Y
B X
B Y
C Y
B Y
C Z
A X
B Y
B Y
A Z
B X
C Y
C Z
B Y
B Y
A Y
B X
B Y
B Y
B X
B Y
C Y
A Y
B Y
C Y
C X
B X
B X
A Z
C Y
B Y
C Z
B X
B Y
B Y
B X
B Y
B Z
B Y
B Y
B X
B Y
B X
C X
B Y
B X
A Y
B Y
B X
B Y
A Y
B X
B X
B Y
A Y
B Y
B Y
B Y
C Z
B X
B Y
B X
B X
B Y
B X
C Z
B Y
B Y
B Y
B Y
B Y
B X
A Y
B Y
C Y
C Z
A Y
B Y
A Y
C Z
B Y
B X
B Y
C X
A Y
B X
B Y
B X
B X
B X
A Y
C Z
B Y
A Y
B X
A Y
B Y
A Y
B X
B Y
B Y
B Y
B X
B X
C Z
B Z
B Y
B X
C Y
C Y
C Z
C X
C Y
B Y
B X
A Y
A Y
B X
C Z
B X
C X
B X
B Y
B Y
A Z
B Z
C Y
C Y
B Y
B Y
C Y
C Y
C Z
B Y
B X
B Y
B Y
C Y
B Y
B Y
B Y
B Y
B Y
C Y
A Z
B X
B Y
C Z
B Y
C Y
B Y
B X
C Y
B Y
B X
C Y
B Y
B Y
B Y
A Y
B X
B X
B Y
B Y
B X
C Z
B Y
A Y
A Y
B X
C X
A Y
B X
B X
B Y
B Y
A Y
C Y
C Z
C Y
B Y
B Y
A Y
A Y
A Y
B Y
B Y
A X
B Y
B Y
B X
B X
C Z
B X
B X
A Y
A Y
A Y
B Y
B Y
C Y
B X
A Y
B Y
C Z
B X
A Y
C Z
A Y
B X
C Y
B Y
B Y
C Y
B X
B X
B Y
B Y
B Y
B Y
A Y
B X
B X
B Y
A Y
B Z
A Y
B Y
C Y
B Y
B Y
B X
C Z
B Y
B Y
B X
B X
C Z
B Y
A Y
B Y
B X
C Y
A Z
C Z
B Y
B Y
B X
C Y
C X
B X
C Y
C Z
B X
B Y
B Y
C Z
B X
C X
A Z
A Y
B X
C X
B Y
A Z
A Z
A Y
B X
A Y
B Y
B Y
C Z
B X
A Z
B Y
B X
A Y
B Y
C Y
B Y
B X
B X
A Z
B Y
B Y
C Z
B X
B X
B Y
C Z
B X
B X
C Z
B X
A Y
B X
C Z
A Y
C X
B Y
B X
B Y
B Y
C Y
B X
A Z
A Y
B X
A Z
B X
B Y
B Y
A Z
C X
B Y
B Y
B Y
A Z
B Y
B X
C Y
C Z
B X
B Y
B Y
B Y
C Y
A Z
B Y
C Z
C X
B Y
C Y
B Y
B X
B Y
B Y
A Y
B Y
B Y
C Z
A Z
B X
C Y
B Y
B Y
B Y
A Y
A Y
B Y
A Y
B Y
A Y
B X
C Y
B Y
C X
A X
B X
A Y
C Y
B Y
A X
B X
A Z
B X
B Y
B Y
B X
B Y
B Y
B X
A Y
A Z
C Z
B Y
B Y
B X
C Z
C Z
B Y
A Y
B X
C Z
A Y
B X
B Z
B Y
B Y
B Y
B X
B Y
B X
B X
B Y
C Y
B Y
B Y
B Y
B Y
B Y
C Z
B X
B Y
B Y
B Y
B X
B X
C Y
B X
B X
C Z
B Y
B Y
B Y
B Y
B Y
C Y
B Y
B Y
B Y
B X
B Y
B X
B Y
B Y
C X
B Y
C X
B X
C Z
C X
B Y
A Y
A Z
A Y
C Y
B X
B Y
B Y
C Z
A Z
B Y
B Y
B Y
B Y
B Y
B Y
B Y
C Y
B Y
C Y
C X
B X
B X
C Z
A X
B X
B Y
A Y
B X
B Y
A Z
B Y
C Y
B X
B Y
B Y
C Y
C Y
B Y
B X
B X
B Y
B Y
B Y
B Y
C Z
B X
B Y
B Y
B X
B Y
B X
B X
B Y
B X
B Y
B Y
C Y
B X
B Y
B Y
B Y
A Y
B Y
A Z
B Y
C Y
C Y
B Y
B X
A X
B Y
A Y
B X
B Y
B Y
B X
C Y
C Z
B X
B Y
A Y
C Y
A Z
C Y
B Y
B Y
B Y
B X
C Y
B Y
B Y
A Y
A X
B Y
B X
B Y
B Y
A Y
B X
C X
B Y
A Y
C Y
B Y
B Y
A Y
C Y
A Y
C Y
B Y
B X
C Y
C Y
B Y
B Y
A Y
B Y
B Y
B Y
C Z
B X
B Y
B X
B X
A X
A Y
B Y
B X
A Z
B X
A Y
B Y
C Y
C Y
C Y
B Y
A Y
A Y
B Y
B Y
B Z
B Y
B X
A Y
B X
A Z
B Y
B Y
B X
B Y
C Y
A Z
B Y
C X
C Y
B Y
B Y
C X
B Y
A Y
A Y
C Z
B X
B X
B X
B X
B Y
C Z
B X
C Y
A Y
B Y
A Y
B Y
A Y
B Y
B Y
C Y
B Y
B Y
B X
B Y
B X
B Y
B X
B Y
A Z
C X
B X
C X
B X
A Y
C Y
B X
C Y
B X
B X
C Z
C Y
B X
B X
B X
B Y
C Y
B X
B X
A Z
B Y
B Y
C Y
B X
C Z
C Y
A Y
B X
C Y
C X
B Y
B Y
A X
B Y
B X
B Y
B X
C Y
B X
A Y
B Y
B X
B Y
B Y
B Y
C Y
C Y
C Y
C Y
B X
B Y
A Z
B X
B X
B Y
B Y
C Z
B Y
B X
B Y
B X
C Y
B Y
C Z
A X
B X
B Y
C Y
C X
B X
B X
B Y
B Y
B Y
B X
B Y
B Y
B X
C Z
B Y
B Y
B X
B X
B Y
B X
C Z
A Z
C X
C X
B Y
B X
A Y
B Y
B X
C Z
A X
B X
B Y
B X
B X
B Y
B Y
A Z
B X
A Y
A Y
B Y
B X
B Y
C Y
A Y
A Y
B X
B Z
C Y
C Y
B Y
C X
B X
C Z
C Z
B Y
C X
A Y
B Y
B X
A Y
B Y
C X
B Y
B X
B Y
C Z
A X
A Z
B Y
B Y
B X
B X
A Y
B Y
B X
B Y
C Y
B Y
B X
C Z
C X
C Y
A Y
B Y
A Y
B Y
B Y
B X
B X
A Y
A Y
B Y
B Y
B Y
A Y
B Y
B Y
B Y
C Z
A Z
C Y
B Y
B X
C Y
A Z
B X
B Y
A Z
C Y
B Y
B X
B Y
B Y
A Y
B X
B Z
B X
B X
B X
B X
B Y
B Y
B X
B Y
C Y
C X
C Z
B Y
B Y
C Y
A Y
B X
B X
B Y
B X
B Y
B Y
A Y
B Y
B Y
B Y
B Y
A Y
B X
C Z
B Y
B Y
B Y
B X
B Y
C Y
B X
B X
A Y
A X
A Y
C X
C Y
B Y
B Y
C Y
B X
B Y
B Y
C Y
B X
C X
B X
C Y
B Y
B X
B X
B Y
C X
B X
B Y
B X
B X
B Y
B X
B Y
B Y
B Y
C Y
B Y
B Y
C Z
B Y
B X
C Y
B Y
B Y
B X
B Y
A Y
B Y
A Y
B Y
B Y
A Z
B X
B Y
B Y
C Z
B X
B X
B Y
B Y
B Y
B X
C Y
C Y
B X
B Z
A X
B Z
C Y
B X
B X
A X
B Y
B X
C Z
C Y
B X
B Y
B Y
B Y
C Z
B Y
C Y
C Y
A Y
B X
B Y
B Y
B Y
A X
B Y
B Y
B X
B X
A Y
B X
B Y
A Z
B Y
C Z
B X
B Y
B Y
A Y
A Y
B Y
B Y
B Y
B Y
C Y
C Z
B X
B X
B Y
B Y
B X
B X
A X
A Y
B Y
B Y
B X
B Y
A Y
B Z
B X
C Z
B Y
B X
B X
B Y
B Y
B Y
C Y
C X
B X
C Z
B Z
B X
B X
C Z
C Y
B X
A Z
C Y
A Y
B X
B Y
C Z
B Y
B Y
B X
B Y
C Z
B Y
A Y
B X
B X
B X
C Y
B X
B Y
B X
B Y
B Y
A X
C Y
A Y
C Y
B X
B Y
B X
B X
B Y
B Y
B Y
B Y
B Y
B Z
B Y
A X
C Z
B X
A Y
C Z
B Y
C X
A Y
C Y
C X
B Y
B X
B X
C Z
C Y
A Z
C Y
A Y
B Z
A Y
B X
C X
A Z
C X
B Y
C X
B Y
A Y
A X
B X
B Y
B X
B X
B X
A Y
B Y
B X
B Y
A X
B Y
C X
B Y
B X
B Y
A Y
B X
B Y
B X
B Y
B X
B Y
B Y
A Z
A X
B Y
C Z
B Y
B Y
B Y
B Y
C Y
B Y
A Y
A Y
C Z
C Y
B Y
A Y
B Y
B X
A Y
C Y
B Y
B Y
A Y
B Y
A X
C X
B Y
B Y
C X
B Y
B X
A X
B Y
B Y
B Y
B X
B X
A Z
B Y
A X
B X
A Z
B X
C Z
B Y
B Y
B Y
B X
B Y
B Y
C Y
B Y
B X
A Y
C Z
B Y
B X
A Y
C Y
B X
B Y
B Y
C Z
A Y
B X
B Y
B X
B X
C X
B Z
C Y
B Y
B Y
B X
B Y
C Y
C Y
C Y
B Y
A Y
C Z
B Y
C X
C Y
B Y
B Y
A Z
B X
A Y
A Y
A Z
B X
A Y
C Z
B Y
B Y
A X
B X
B Y
C Z
B Y
B Y
B X
B Y
B X
B X
A X
C Y
C Y
C Y
B Y
B Y
C Z
B Y
B X
C X
B Y
C Z
B X
B Y
B Y
B Y
B X
B Y
B X
B X
B Y
B Y
B Y
B Y
B X
B Y
B Y
C Z
B X
B Y
C Y
B X
B Z
B Y
C Z
C Y
B Y
A Z
A Y
B X
B Y
C Y
A X
A Y
B X
B Y
C Z
B Y
C X
A Y
C Y
B Y
B X
B Y
B Y
B Y
B X
B Y
C X
A Z
B X
C Y
A Y
B X
B Y
B X
B Y
C X
A Y
A Y
C Z
B Y
C Y
B Y
B Y
B Y
B Y
B Y
C Y
A Y
B Y
B X
C Y
B Y
B Y
A Z
B Y
B Y
B X
B Y
B Y
B X
A Y
A Z
B X
B X
C Y
B Y
B X
C Y
B Y
A X
B X
B Y
A Z
B Y
B Y
B Y
B Y
B X
A X
B X
C Y
B Y
B Y
B X
C Y
B Y
B X
B Y
B X
A X
B Y
A Y
B X
C X
B Y
C Z
B Y
B Y
C Y
B Y
C X
B Y
B X
A Z
B Y
B X
B Y
A Y
B Y
B X
B X
B X
B Y
B Y
B Y
A Y
C X
B X
B X
C Z
B Y
A Y
A Z
A Y
B Y
B Y
B X
C X
C Y
C Z
B Y
B Y
B Y
B Y
B Y
B X
C Y
B Y
B Y
B X
B X
B Y
B Y
A Y
A Y
A Y
B X
B X
C Y
B Y
A Z
B X
C Y
B Y
B X
B Y
B Y
A Y
A Y
B Y
B Y
B X
B X
A Y
A X
A Z
C X
A Z
B X
B Y
C Y
A X
B X
C Z
B Y
C Y
A Y
C X
B Y
C X
A Y
B Y
B X
B Y
A X
B X
B X
B Y
B Y
B Y
B X
B Y
B X
B Y
A X
B Y
B X
B Y
B Y
B Y
B X
B X
A Y
B Y
A Z
B Y
B X
C Z
B X
B Y
B Y
B Y
B X
C Y
B Y
B Y
A Y
B X
B X
B Y
B Y
A Y
B Y
B X
B Y
B X
B Y
C X
C Y
B X
B X
B X
C Z
B Y
B Y
B X
B X
B Y
A Y
B Y
C X
A Y
B Y
B Y
C X
B X
A Y
C X
B Y
B X
C Z
B X
B Y
A Y
B Y
B X
C Y
A Y
B Y
A X
B Y
C Y
C X
B Y
B X
A Z
B Y
B Y
B X
B Y
B Y
B X
B Y
C Y
B X
B Y
B X
B X
C Y
B X
B X
A Y
B X
B Y
B Y
B Y
B Y
B Y
B Y
B Y
C X
B X
B X
A Y
B Y
A Y
B X
B Y
A Y
B Y
A Z
B X
A Y
C Z
A Y
A Z
B X
B Y
A Y
B X
B X
B Y
B Y
A Z
A Y
B X
C Y
B Y
B Z
C X
C X
B X
A Y
B X
B Y
B Y
A X
B Y
A X
B Y
A Y
B X
B X
A Z
A Y
A Y
C Z
B Y
B Y
C Z
B Y
B X
C Y
B Y
B X
A Y
B Y
B X
C X
C X
B Y
A Y
B Y
B Y
B Y
B X
A Y
B Y
B Y
A Y
B Y
B X
B X
C Y
C X
B Y
C X
B Y
C Y
B X
B Y
B X
B Y
B Y
B X
B Y
B Y
C Y
B X
B Y
B X
B Y
A Y
B X
A Y
B X
B Y
B X
C X
C Y
B Y
B X
B Y
B Y
B X
B Y
B Y
A Y
B Y
B X
B Y
B X
C Y
A Y
B Y
B X
B Z
B Y
B X
C Y
B Y
C Y
C Y
B X
C Z
B X
C Y
B Y
A Y
B Y
A X
B Y
B Y
B Y
B Y
A Z
B Y
B Y
A Y
C Y
B Y
B X
B Y
B X
B Y
B Z
B X
B X
B Y
B Y
B Y
B X
B Y
B X
B Y
B Y
A Y
C Z
B Y
B Y
B X
B X
B X
B Y
A Y
A Y
B X
B Y
B X
A X
B Y
B Y
C Y
A Y
C Z
A Z
A Y
B Y
B Y
B Y
B Y
B Y
C X
B Y
A Y
C X
C Y
B X
A Z
C Z
A Z
C Y
B X
B Y
B Y
B X
B Y
A Z
C Z
C X
B X
B Z
A Y
C Y
C Y
C Y
A Y
C X
B X
C Y
C Y
B Y
B Y
A Y
B Y
A Y
A Y
B X
B X
C Y
B Y
C Y
B Y
B Z
B Y
A Y
B X
B Y
A X
B X
B Y
B Y
C Y
B Y
C Z
B Z
A Y
A Y
A Y
B Y
B X
B Y
A Y
C X
B X
B Y
B X
C X
B Y
B X
B Y
B Y
B X
A Y
A Y
B Y
B Y
B Y
A Z
B Y
B Y
B Y
B Y
B Y
B X
B Y
B Y
B Y
B Y
B Y
B X
B X
B X
A X
C Y
C X
C Z
C Y
B X
B Y
A Z
B Y
C Y
B Y
B X
B Y
A Y
B X
B X
B X
C Y
B Y
B Y
B Y
B X
B Y
B Y
B Y
B Y
B Y
B Y
C X
B Y
A X
B X
C Z
B X
B Y
B X
B Y
C Y
B Y
B Y
B X
A Z
B Y
A X
B Y
C Z
C Y
B Y
B Y
B Y
C X
B Y
B Y
B X
A Y
C Z
B Y
B X
B Y
B Y
B Y
B X
B Y
B Y
B Y
C X
B X
B X
C Z
B Y
B Y
B X
A Z
B Y
B Y
C Y
C Y
A Y
C Y
A Y
B Y
B X
B Y
B X
C Y
B Y
B Y
B Y
B Y
B Y
C X
B X
B X
B Y
C X
C Z
B X
A Y
C Z
B X
B X
C Y
C Y
A Y
B Y
B X
B Y
B Y
A Z
A Z
B Y
B Y
B Y
B Y
B Y
B Y
B Y
B X
B Y
C Y
B Y
B X
A X
B Y
A Y
A Y
B Y
B Y
B X
B Y
B Y
C Y
A Y
B X
B X
B X
B Y
B Y
B Y
B Y
B X
B X
A Y
B X
B X
B X
B X
B Y
B X
A X
C Y
B Y
B Y
A Y
B Y
B X
C X
C Y
A Y
B Y
A Z
C Y
B Y
B Y
B Y
B X
B X
B Y
C X
B X
B Y
C X
B X
A Y
B Y
B X
B Y
B Y
B X
B Y
B Y
C Y
B X
B X
B X
A Y
B Y
B X
C Y
C Y
B X
A Y
B Y
C Y
B X
B Y
B X
B X
B Y
C Y
A Y
C Y
B X
C X
B Y
B X
A Y
C Y
B Y
B Y
B Y
C Z
C Y
A Z
A Y
B Y
B Y
B Y
B Y
A Y
B X
B Y
B Y
C Y
C X
B Y
B Y
B Y
B Y
B X
B X
B X
C Z
B Y
B Y
C Y
B X
B Y
B Y
A Z
B Y
C Z
B X
A Y
B X
B Y
A Y
A Z
A Z
B Z
B Y
B Y
A Y
C Z
B Y
C Z
B X
B Y
B Y
B Y
B Y
C Y
B X
B X
B X
B X
B X
B Y
A Z
A Y
B Y
B Y
B Y
C X
B Y
A Y
B Y
B Y
B X
B Y
C Y
A Z
A Y
C Y
C Z
B X
A Z
B X
B X
B Z
B Y
C Y
A Y
B Y
B Y
B X
C Z
B Y
B Y
A Z
A X
B Y
B X
B Y
B X
B X
B X
B X
A Y
B Y
A X
B X
B X
B Y
B X
B Y
B Y
A Y
B Y
C Y
A Z
A Y
B X
B Y
A Y
C X
B Y
C Y
B X
B Y
A Y
B Y
A Z
B Y
B Y
A Y
B X
C Y
B Y
B Y
C Z
B X
B Z
B Y
A Y
B Y
C X
B Y
B Y
B Y
B Y
B Y
C Z
C Z
B Y
C Y
C Z
A X
B Y
A Y
B X
B X
B Z
B X
A Y
B Y
B Y
B Y
A Z
C Y
B Y
B Y
C Y
C Z
C X
B Y
A X
B Y
A Y
C X
B Y
B Y
B Y
B Z
B X
B X
C Y
B X
B X
C Z
B Y
B X
B X
B Y
B Y
B X
C X
B Y
B Y
B X
A Y
B Y
C Y
B Y
A X
B Y
A Y
A Y
B Y
B X
B X
C X
B Y
B X
A Y
C X
A Y
B X
B Y
B Y
C Z
B X
B Y
B X
B Y
B Y
A Z
B Z
B Y
B Y
C Y
C X
C Y
C Y
B Y
B Y
B Y
C Y
A Z
A Z
B Y
B X
A Y
B X
B Y
A Y
B X
B Y
B X
C X
B Y
B Y
B X
B X
A Z
A Y
B Y
A Y
B Y
B X
B X
A Y
B X
B Y
B Y
B X
C X
C X
B Y
B Y
A Y
B X
B Y
B Y
B Y
B Y
C Y
B Y
C Z
B Y
B Y
C X
B X
B Y
B Y
B X
B X
B Y
B Y
B Y
B X
A Z
B Y
B X
C Z
B X
B Y
A Z
C Z
A Z
B X
B Y
B Y
B Y
B X
B Y
C Y
C X
C Y
A X
B Y
B Z
B Y
B Y
B Y
A Y
B X
B Y
C Y
B Y
B X
B X
B Y
B Y
B Y
C Z
B Y
B X
B Z
B X
B Y
B Y
B X
B X
A Y
B X
B X
B X
A Y
B X
B X
B Y
B X
A X
B Y
B Y
C Y
B X
B Y
B X
B X
C Y
B Y
B Y
B X
A X
C Y
C X
A Y
B X
B Y
B Y
B Y
B Y
B X
B Y
B Y
B Y
B Y
C Y
C Z
B Y
C X
B X
B Y
A Z
C X
B X
B Y
B Y
B X
B Y
B Y
B Y
B Y
B Y
B Y
B Y
C Y
B Y
C Y
B X
A Z
B Y
B X
A Y
B Y
B X
A Y
B X
B X
B X
B Y
B Y
B X
B Y
A Z
B Y
B Y
B Y
B Y
B Y
B Y
B Y
B Y
B X
B Y
B Y
A Y
B Y
B X
B X
C Y
C X
B Y
A Y
C Z
B X
B X
B Y
C Y
A Y
B Y
B Y
B X
B Y
B X
C Y
C Y
B Y
B X
B X
B Y
C Y
B Y
C Y
B Y
B Y
C Y
A Y
B Y
A Z
C X
B Y
B Y
B X
B X
C Z
B Y
B Y
B Y
B X
B X
A X
B X
B Z
B Y
B X
B X
B Y
B X
B X
B Y
B Y
B Y
B Y
A Y
B Y
B X
B Z
B Y
A X
A X
A Y
B Y
B Y
C Y
A Y
C Y
B Y
B X
B Y
B Y
B X
B Y
A Y
B Y
B Y
B X
B Y
A Y
B X
B Y
"""
parsed = [strat.strip().split(" ") for strat in strats.split("\n")][:-1]
run_strategy_pt1(parsed)
run_strategy_pt2(parsed)
