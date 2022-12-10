# https://adventofcode.com/2022/day/7

import heapq
from dataclasses import dataclass, field

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    terminal_output = [line.split() for line in file.readlines()]


@dataclass
class Dir:
    name: str
    parent: None = None
    subdirs: dict = field(default_factory=dict)
    files: dict = field(default_factory=dict)


def build_tree(terminal_output):
    root = Dir('/')
    curr_dir = None
    ls = False
    for line in terminal_output:
        if line[0] == '$':
            ls = False
            if line[1] == 'cd':
                if line[2] == '/':
                    curr_dir = root
                elif line[2] == '..':
                    curr_dir = curr_dir.parent
                else:
                    curr_dir = curr_dir.subdirs[line[2]]
            elif line[1] == 'ls':
                ls = True
        elif ls:
            if line[0] == 'dir':
                curr_dir.subdirs[line[1]] = Dir(line[1], curr_dir)
            else:
                curr_dir.files[line[1]] = int(line[0])
    return root


def folder_sizes(fs):
    sizes_ascending = []
    def size(curr_dir):
        file_sizes = sum(curr_dir.files.values())
        subdir_sizes = sum(size(subdir) for subdir in curr_dir.subdirs.values())
        total_size = file_sizes + subdir_sizes
        heapq.heappush(sizes_ascending, total_size)
        return total_size
    root_size = size(fs)
    return sizes_ascending, root_size


# Part 1

fs = build_tree(terminal_output)
sizes_sorted, root_size = folder_sizes(fs)

sizes = sizes_sorted.copy()
sum_under_100k = 0
while True:
    curr = heapq.heappop(sizes)
    if curr <= 100000:
        sum_under_100k += curr
    else:
        break
print(sum_under_100k)


# Part 2

DISK_SPACE = 70000000
SPACE_REQUIRED = 30000000

sizes = sizes_sorted.copy()
while True:
    size = heapq.heappop(sizes)
    if size + (DISK_SPACE - root_size) >= SPACE_REQUIRED:
        print(size)
        break