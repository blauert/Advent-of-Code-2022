# https://adventofcode.com/2022/day/4

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    pairs = [line.strip().split(',') for line in file.readlines()]


contain_count = 0
overlap_count = 0

for pair in pairs:
    elf1 = [int(i) for i in pair[0].split('-')]
    elf2 = [int(i) for i in pair[1].split('-')]
    sections1 = set(range(elf1[0], elf1[1]+1))
    sections2 = set(range(elf2[0], elf2[1]+1))
    # Part 1
    if sections1 <= sections2 or sections2 <= sections1:
        contain_count += 1
    # Part 2
    if sections1 & sections2:
        overlap_count += 1

print(contain_count)
print(overlap_count)