class Robot:
    def __init__(self, x, y, vx, vy, width, height):
        self.x = x
        self.y = y
        self.v = (vx, vy)
        self.size = (width, height)
    
    def move(self):
        self.x = (self.x + self.v[0]) % self.size[0]
        self.y = (self.y + self.v[1]) % self.size[1]
    
    def move_n(self, n):
        mod_width = n % self.size[0]
        mod_height = n % self.size[1]
        self.x = (self.x + mod_width*self.v[0]) % self.size[0]
        self.y = (self.y + mod_height*self.v[1]) % self.size[1]

    def get_pos(self):
        return (self.x, self.y)

    def get_quad(self):
        mid = (self.size[0] // 2, self.size[1] // 2)
        if self.x == mid[0] or self.y == mid[1]:
            return 0
        
        # quad numbers:
        # 1 2
        # 3 4
        quad = 1
        # add 1 if we cross from left to right
        if self.x > mid[0]:
            quad += 1
        
        # add 2 if we cross from top to bottom
        if self.y > mid[1]:
            quad += 2
        return quad

def get_safety_factor(robots, n):
    quads = [0, 0, 0, 0, 0]
    for robot in robots:
        robot.move_n(n)
        quads[robot.get_quad()] += 1
    
    total = 1
    for i in range(1, len(quads)):
        total *= quads[i]
    return total

def parse(filename):
    width = 0
    height = 0
    robots = []
    with open(filename, 'r') as file:
        # edit input file to add width and height
        dim = file.readline().strip().split(',')
        width = int(dim[0])
        height = int(dim[1])

        for line in file:
            posstr, velstr = line.strip().split()
            posarr = posstr[2:].split(',')
            velarr = velstr[2:].split(',')
            robots.append(
                Robot(int(posarr[0]), int(posarr[1]), int(velarr[0]), int(velarr[1]), width, height)
            )
    return robots, height, width

def pprint_robots(robots, h, w):
    pos = {robot.get_pos() for robot in robots}
    for r in range(h):
        s = ''
        for c in range(w):
            if (c, r) in pos:
                s += '@'
            else:
                s += ' '
        print(s)

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    robots, height, width = parse(filename)
    print(get_safety_factor(robots, 100))

    robots, height, width = parse(filename)
    seconds = 0
    no_overlap = len(robots)
    while seconds < 10302:
        pos = len({robot.get_pos() for robot in robots})
        if pos == no_overlap:
            print(f'Seconds: {seconds}, unique: {pos}')
            pprint_robots(robots, height, width)
            max_pos = pos
        seconds += 1
        for robot in robots:
            robot.move()