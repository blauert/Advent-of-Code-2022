# https://adventofcode.com/2022/day/5

import copy
from itertools import dropwhile, takewhile

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip('\n') for line in file.readlines()]

commands = [c for c in dropwhile(lambda x: x[:4] != 'move', lines)]

cargo = takewhile(lambda x: not x[1].isdigit(), lines)
crates = [c for c in zip(*cargo)]
stacks = {}
curr_stack = 1
for i in range(1, len(crates), 4):
    stacks[curr_stack] = [c for c in takewhile(lambda x: x != ' ', reversed(crates[i]))]
    curr_stack += 1


# Part 1

stacks9000 = copy.deepcopy(stacks)
for c in commands:
    _, quantity, _, source, _, destination = c.split()
    for i in range(int(quantity)):
        stacks9000[int(destination)].append(stacks9000[int(source)].pop())

print(''.join([stacks9000[i][-1] for i in range(1, len(stacks9000)+1)]))


# Part 2

stacks9001 = copy.deepcopy(stacks)
for c in commands:
    _, quantity, _, source, _, destination = c.split()
    stacks9001[int(destination)].extend(stacks9001[int(source)][-int(quantity):])
    del stacks9001[int(source)][-int(quantity):]

print(''.join([stacks9001[i][-1] for i in range(1, len(stacks9001)+1)]))
