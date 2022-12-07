import re

test = False
part1_algo = False
filename = "input.txt"

if test:
    filename = "test.txt"

crates = []
commands = []
with open(filename, 'r') as file:
    for raw_line in file:
        line = raw_line.strip("\r\n")
        if len(line) > 0:
            if line[0] == 'm':
                commands.append([int(x) for x in re.findall(r'\d+', line)])
                # adjust crate stack indicators to be used as indicies
                commands[-1][1] -= 1
                commands[-1][2] -= 1
            elif line.find('[') > -1:
                # initialize empty crate stacks
                if len(crates) == 0:
                    count_crates = (len(line) // 4) + 1
                    for idx in range(0, count_crates):
                        crates.append([])

                # go through line and append crates
                for idx in range(0, len(crates)):
                    line_idx = (idx * 4) + 1
                    if not line[line_idx].isspace():
                        crates[idx].append(line[line_idx])

# reverse the crate stacks since they got built from bottom to top
for idx in range(0, len(crates)):
    crates[idx] = crates[idx][::-1]

# run the commands
if part1_algo:
    for command in commands:
        for _ in range(0, command[0]):
            crates[command[2]].append(crates[command[1]].pop())
else:
    for command in commands:
        crane = []
        for _ in range(0, command[0]):
            crane.append(crates[command[1]].pop())

        for _ in range(0, command[0]):
            crates[command[2]].append(crane.pop())

print(crates)

answer = ""
for crate in crates:
    answer += crate.pop()
print(answer)
        
            
    
