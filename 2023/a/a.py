import re

numbers = re.compile('(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))')

result_to_int = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}

def convert(match):
    if match in result_to_int.keys():
        return result_to_int[match]
    else:
        return int(match)

def main():
    test = False
    filename = "./a/input.txt"

    if test:
        filename = "./a/test.txt"

    ret = []
    i = 1
    with open(filename, 'r') as file:
        for rawline in file:
            matches = numbers.findall(rawline)
            ret.append(convert(matches[0])*10 + convert(matches[-1]))
            i = i + 1

    print(sum(ret))


if __name__ == "__main__":
    main()
