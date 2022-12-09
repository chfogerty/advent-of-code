def unique(s):
    return len(set(s)) == len(s)

def find_start_of_packet(line, window=4):
    for idx in range(window, len(line)):
        if unique(line[idx-window:idx]):
            return idx
    return -1


test = False
filename = "./f/input.txt"

if test:
    filename = "./f/test.txt"

with open(filename, 'r') as file:
    for line in file:
        print(find_start_of_packet(line), find_start_of_packet(line, 14))