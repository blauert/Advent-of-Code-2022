# https://adventofcode.com/2022/day/7

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
    sizes = []
    def size(curr_dir):
        file_sizes = sum(curr_dir.files.values())
        subdir_sizes = sum(size(subdir) for subdir in curr_dir.subdirs.values())
        total_size = file_sizes + subdir_sizes
        sizes.append(total_size)
        return total_size
    size(fs)
    return sizes


# Part 1

fs = build_tree(terminal_output)
sizes = folder_sizes(fs)

print(sum(s for s in sizes if s <= 100000))


# Part 2

DISK_SPACE = 70000000
SPACE_REQUIRED = 30000000

sizes.sort()
for size in sizes:
    if size + (DISK_SPACE - sizes[-1]) >= SPACE_REQUIRED:
        print(size)
        break