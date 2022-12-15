# https://adventofcode.com/2022/day/13

import json
from functools import cmp_to_key

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = file.readlines()

packets = []
for i in range(0, len(lines), 3):
    packets.append(json.loads(lines[i]))
    packets.append(json.loads(lines[i+1]))


def zip_shortest_longest(left, right):
    len_l, len_r = len(left), len(right)
    for i in range(min(len_l, len_r)):
        yield left[i], right[i]
    if len_l > len_r:
        yield left[len_r], None
    elif len_r > len_l:
        yield None, right[len_l]


def check_order(packets):
    stack = [i for i in reversed(list(zip_shortest_longest(*packets)))]
    while stack:
        left, right = stack.pop()
        if left is None:
            return True
        if right is None:
            return False
        if isinstance(left, int) and isinstance(right, int):
            if left > right:
                return False
            if left < right:
                return True
        elif isinstance(left, int):
            left = [left]
        elif isinstance(right, int):
            right = [right]
        if isinstance(left, list) and isinstance(right, list):
            q = []
            for l, r in zip_shortest_longest(left, right):
                q.append((l, r))
            for pair in reversed(q):
                stack.append(pair)


# https://docs.python.org/3/library/functools.html#functools.cmp_to_key
# A comparison function is any callable that accepts two arguments
def compare_packets(left, right):
    # compares them
    if check_order([left, right]):
        # and returns a negative number for less-than
        return -1
    # zero for equality
    ## (there are no equal packets in the input)
    else:
        # or a positive number for greater-than
        return 1


# Part 1

sum_of_indices = 0
index = 1
for i in range(0, len(packets), 2):
    if check_order([packets[i], packets[i+1]]):
        sum_of_indices += index
    index += 1
print(sum_of_indices)


# Part 2

packets.append([[2]])
packets.append([[6]])

# https://docs.python.org/3/howto/sorting.html#comparison-functions
packets = sorted(packets, key=cmp_to_key(compare_packets))

decoder_key = 1
for i, packet in enumerate(packets, start=1):
    if packet == [[2]] or packet == [[6]]:
        decoder_key *= i
print(decoder_key)