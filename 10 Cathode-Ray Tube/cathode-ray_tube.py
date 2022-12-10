# https://adventofcode.com/2022/day/10

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    instructions = [line.split() for line in file.readlines()]


# Part 1

def is_20_or_40eth(cycle):
    if cycle == 20 or (cycle - 20) % 40 == 0:
        return True
    return False


def signal_strengths():
    cycle = 0
    x = 1
    signal_strengths = 0

    for ins in instructions:
        cycle += 1
        if is_20_or_40eth(cycle):
            signal_strengths += cycle * x
        if ins[0] == 'addx':
            cycle += 1
            if is_20_or_40eth(cycle):
                signal_strengths += cycle * x
            x += int(ins[1])
    return signal_strengths


print(signal_strengths())


# Part 2

def draw_pixel(cycle, x, row, crt):
    curr_pixel = cycle % 40
    if curr_pixel in {x-1, x, x+1}:
        crt[row][curr_pixel] = '#'
    cycle += 1
    if cycle % 40 == 0:
        row += 1
    return cycle, row, crt


def draw_crt():
    cycle = 0  # current pixel
    x = 1  # middle of sprite position
    crt = [['.' for i in range(40)] for j in range(6)]
    row = 0
    for ins in instructions:
        cycle, row, crt = draw_pixel(cycle, x, row, crt) 
        if ins[0] == 'addx':
            cycle, row, crt = draw_pixel(cycle, x, row, crt)
            x += int(ins[1])
    return crt


for row in draw_crt():
    print(' '.join(row))