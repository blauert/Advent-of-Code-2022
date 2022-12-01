# https://adventofcode.com/2022/day/1

input_file = "real_input.txt"
# input_file = 'test_input.txt'

with open(input_file) as file:
    calories = file.readlines()

calories.append("")

curr = 0
max_cal = 0
elves = []
for cal in calories:
    cal = cal.strip()
    if cal:
        curr += int(cal)
    else:
        if curr > max_cal:
            max_cal = curr
        elves.append(curr)
        curr = 0

# Part 1
print(max_cal)

# Part 2
elves.sort()
print(sum(elves[-3:]))
