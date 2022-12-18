# https://adventofcode.com/2022/day/9

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    motions = [line.split() for line in file.readlines()]


def move_head(position, direction):
    x, y = position
    if direction == 'U':
        y += 1
    elif direction == 'R':
        x += 1
    elif direction == 'D':
        y -= 1
    elif direction == 'L':
        x -= 1
    return x, y


def move_tail(head_position, tail_position):
    hx, hy = head_position
    tx, ty = tail_position
    if abs(hx - tx) == 2 and abs(hy - ty) == 2:
        #  . . H      . . H
        #  . . .  ->  . T .
        #  T . .      . . .
        tx += (hx - tx) // 2
        ty += (hy - ty) // 2
    elif abs(hx - tx) == 2:
        #  . . .      . . .        . . .      . . .
        #  T . H  ->  . T H   or   . . H  ->  . T H
        #  . . .      . . .        T . .      . . .
        tx += (hx - tx) // 2
        ty = hy
    elif abs(hy - ty) == 2:
        #  . H .      . H .        . H .      . H .
        #  . . .  ->  . T .   or   . . .  ->  . T .
        #  . T .      . . .        T . .      . . .
        ty += (hy - ty) // 2
        tx = hx
    return tx, ty


# Part 1

head_position = (0, 0)
tail_position = (0, 0)
tail_visited = {(0, 0)}

for direction, steps in motions:
    for i in range(int(steps)):
        head_position = move_head(head_position, direction)
        tail_position = move_tail(head_position, tail_position)
        tail_visited.add(tail_position)

print(len(tail_visited))


# Part 2

knots = {i: (0, 0) for i in range(10)}
tail_visited = {(0, 0)}

for direction, steps in motions:
    for i in range(int(steps)):
        knots[0] = move_head(knots[0], direction)
        for i in range(1, 10):
            new_pos = move_tail(knots[i-1], knots[i])
            if knots[i] == new_pos:  # No need to calculate following knots
                break
            knots[i] = new_pos
        tail_visited.add(knots[9])

print(len(tail_visited))