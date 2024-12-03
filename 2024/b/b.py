def p1_is_safe(report):
    increasing = report[0] < report[1]
    current = report[0]
    for next in report[1:]:
        diff = next - current
        if abs(diff) > 3 or diff == 0 or (current < next) != increasing:
            return False
        current = next
    return True

def p2_is_safe(report):
    if p1_is_safe(report):
        return True
    
    for i in range(0, len(report)):
        if p1_is_safe(report[:i] + report[i+1:]):
            return True
    return False


def parse(filename):
    readings = []
    with open(filename, 'r') as file:
        for line in file:
            values = line.strip().split()
            readings.append([int(v) for v in values])
    return readings

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    p1_safe = 0
    p2_safe = 0
    reports = parse(filename)
    for report in reports:
        if p1_is_safe(report):
            p1_safe += 1
        if p2_is_safe(report):
            p2_safe += 1
    print(p1_safe)
    print(p2_safe)
