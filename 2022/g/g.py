import re

CD = re.compile(r"\$ cd (.+)")
LS = re.compile(r"\$ ls")
DIR = re.compile(r"dir (.+)")
FILE = re.compile(r"(.+) (.+)")

DISK_SIZE = 70000000
NEEDED_SPACE = 30000000

class Node:
    def __init__(self, name, type, size = 0):
        self.name = name
        self.size = size
        self.type = type
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def get_size(self):
        if self.size == 0:
            for child in self.children:
                self.size += child.get_size()
        return self.size

    def __str__(self):
        return f"{self.type} {self.get_size()}"
    
    def max_filter_tree(self, types, max_size):
        pass_filter = []
        for child in self.children:
            pass_filter.extend(child.max_filter_tree(types, max_size))
        if (self.get_size() <= max_size) and (self.type in types):
            pass_filter.append(self.size)
        return pass_filter
    
    def min_filter_tree(self, types, min_size):
        pass_filter = []
        for child in self.children:
            pass_filter.extend(child.min_filter_tree(types, min_size))
        if (self.get_size() >= min_size) and (self.type in types):
            pass_filter.append(self.size)
        return pass_filter
    
    def get_child(self, child_name):
        for child in self.children:
            if child.name == child_name:
                return child
        return None

test = False
filename = "./g/input.txt"

if test:
    filename = "./g/test.txt"

pt1_total = 0
root = None

with open(filename, 'r') as file:
    cur_dir = None
    for line in file:
        if m := re.match(CD, line):
            dir = m.group(1)
            if root == None:
                root = Node(dir, "dir")
                cur_dir = root
            elif dir == '..':
                cur_dir = cur_dir.parent
            else:
                cur_dir = cur_dir.get_child(dir)
        elif m := re.match(LS, line):
            pass
        elif m := re.match(DIR, line):
            node = Node(m.group(1), "dir")
            cur_dir.add_child(node)
        elif m := re.match(FILE, line):
            node = Node(m.group(2), "file", int(m.group(1)))
            cur_dir.add_child(node)

pt1_match = root.max_filter_tree(["dir"], 100000)
print(sum(pt1_match))

unused_space = DISK_SIZE - root.get_size()
space_to_free = NEEDED_SPACE - unused_space

pt2_match = root.min_filter_tree(["dir"], space_to_free)
pt2_match.sort()
print(pt2_match[0])