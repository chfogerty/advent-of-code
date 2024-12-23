from collections import deque

MEMO = dict()

def prune(number):
    return number % 16777216

def mix(number, res):
    return number ^ res

def next_secret_number(number):
    initial = number
    if number in MEMO:
        return MEMO[number]

    res = number << 6
    number = prune(mix(number, res))
    res = number >> 5
    number = prune(mix(number, res))
    res = number << 11
    number = prune(mix(number, res))

    MEMO[initial] = number
    return number

def calc_nth_secret(number, n):
    prices = [number % 10]
    for _ in range(n):
        number = next_secret_number(number)
        prices.append(number % 10)
    return number, prices

def p1(initial_numbers):
    total = 0
    all_prices = dict()
    for number in initial_numbers:
        final, prices = calc_nth_secret(number, 2000)
        total += final
        all_prices[number] = prices
    return total, all_prices

def p2(all_prices):
    price_sequences = dict()
    for secret in all_prices:
        prices = all_prices[secret]
        dq = deque()
        found_sequences = set()
        for idx in range(1, len(prices)):
            price = prices[idx]
            if len(dq) == 4:
                dq.popleft()
            dq.append(price - prices[idx - 1])
            if len(dq) == 4:
                sequence = tuple(dq)
                if sequence not in found_sequences:
                    found_sequences.add(sequence)
                    if sequence not in price_sequences:
                        price_sequences[sequence] = 0
                    price_sequences[sequence] += price

    max_banana = 0
    for sequence in price_sequences:
        if price_sequences[sequence] > max_banana:
            max_banana = price_sequences[sequence]
    return max_banana


def parse(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return [int(line.strip()) for line in lines]

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    initial_numbers = parse(filename)
    total, all_prices = p1(initial_numbers)
    print(total)
    print(p2(all_prices))
