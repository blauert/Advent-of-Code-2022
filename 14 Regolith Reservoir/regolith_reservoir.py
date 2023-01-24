# https://adventofcode.com/2022/day/14

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    scan = [[[int(c) for c in coords.split(',')] for coords in line.strip().split(' -> ')] for line in file.readlines()]


START = (500, 0)

rocks = set()
bottom = 0

for rock in scan:
    for start, end in zip(rock[:-1], rock[1:]):
        if start[0] == end[0]:
            x = start[0]
            y_min, y_max = sorted([start[1], end[1]])
            if y_max > bottom:
                bottom = y_max
            for y in range(y_min, y_max+1):
                rocks.add((x, y))
        else:
            y = start[1]
            if y > bottom:
                bottom = y
            x_min, x_max = sorted([start[0], end[0]])
            for x in range(x_min, x_max+1):
                rocks.add((x, y))


def is_free(coords):
    if (coords not in rocks) and (coords not in resting_sand):
        return True
    else:
        return False


def down(coords):
    x, y = coords
    return (x, y+1)


def down_left(coords):
    x, y = coords
    return (x-1, y+1)


def down_right(coords):
    x, y = coords
    return (x+1, y+1)


## Part 1

resting_sand = set()
falling_sand = False

while not falling_sand:
    sand = START
    while True:
        if is_free(down(sand)):
            sand = down(sand)
        elif is_free(down_left(sand)):
            sand = down_left(sand)
        elif is_free(down_right(sand)):
            sand = down_right(sand)
        else:
            resting_sand.add(sand)
            break
        if sand[1] == bottom:
            falling_sand = True
            break

print(f"Part 1: {len(resting_sand)}")


## Part 2

floor = bottom + 2

resting_sand = set()
reached_start = False

while not reached_start:
    sand = START
    while True:
        if is_free(down(sand)) and not down(sand)[1] == floor:
            sand = down(sand)
        elif is_free(down_left(sand)) and not down_left(sand)[1] == floor:
            sand = down_left(sand)
        elif is_free(down_right(sand)) and not down_right(sand)[1] == floor:
            sand = down_right(sand)
        else:
            resting_sand.add(sand)
            if sand == START:
                reached_start = True
            break

print(f"Part 2: {len(resting_sand)}")