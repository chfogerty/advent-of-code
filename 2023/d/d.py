# returns [(set of winning numbers, list of numbers)]
def parse(filename):
    with open(filename, 'r') as file:
        cards = []
        for rawline in file:
            card = rawline.split(':')[1].strip().replace('  ', ' ').split(' | ')
            winning_numbers = {int(i) for i in card[0].split(' ')}
            card_numbers = [int(i) for i in card[1].split(' ')]
            cards.append((winning_numbers, card_numbers))
    return cards

def part_1(cards):
    total = 0
    for card in cards:
        correct = 0
        for n in card[1]:
            if n in card[0]:
                correct += 1
        if correct > 0:
            total += 2**(correct - 1)
    return total

def winnings(card):
    total = 0
    for n in card[1]:
        if n in card[0]:
            total += 1
    return total

def part_2(cards):
    card_counts = [1 for _ in range(len(cards))]
    for idx in range(len(cards)):
        card = cards[idx]
        new_cards = winnings(card)
        add = idx + 1
        while new_cards > 0:
            card_counts[add] += card_counts[idx]
            new_cards -= 1
            add += 1
    return sum(card_counts)


def main():
    test = False
    filename = "./d/input.txt"

    if test:
        filename = "./d/test.txt"

    cards = parse(filename)
    print(part_1(cards))
    print(part_2(cards))

if __name__ == "__main__":
    main()