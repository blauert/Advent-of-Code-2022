# https://adventofcode.com/2022/day/3

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    rucksacks = [line.strip() for line in file.readlines()]


def get_priority(item):
    if item.islower():
        priority = ord(item) - 96
    else:
        priority = ord(item) - 38
    return priority


# Part 1

sum_of_priorities = 0

for sack in rucksacks:
    half = len(sack)//2
    item = ''.join(set(sack[:half]) & set(sack[half:]))
    sum_of_priorities += get_priority(item)

print(sum_of_priorities)


# Part 2

sum_of_priorities = 0

for i in range(0, len(rucksacks), 3):
    sack1, sack2, sack3 = rucksacks[i], rucksacks[i+1], rucksacks[i+2]
    item = ''.join(set(sack1) & set(sack2) & set(sack3))
    sum_of_priorities += get_priority(item)

print(sum_of_priorities)
