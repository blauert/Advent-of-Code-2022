# https://adventofcode.com/2022/day/2

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    rounds = [line.split() for line in file.readlines()]

shape_codes = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
    'X': 'R',
    'Y': 'P',
    'Z': 'S'
}

shape_scores = {
    'R': 1,
    'P': 2,
    'S': 3
}

winning_shapes = {
    'R': 'S',
    'P': 'R',
    'S': 'P'
}


# Part 1

total_score = 0
for shapes in rounds:
    opponent, player = shape_codes[shapes[0]], shape_codes[shapes[1]]
    total_score += shape_scores[player]
    if player == opponent:
        total_score += 3
        continue
    if winning_shapes[player] == opponent:
        total_score += 6

print(total_score)


# Part 2

losing_shapes = {
    'R': 'P',
    'P': 'S',
    'S': 'R'
}

total_score = 0
for opp_shape, player_move in rounds:
    opponent = shape_codes[opp_shape]
    # lose
    if player_move == 'X':
        player = winning_shapes[opponent]
    # draw
    elif player_move == 'Y':
        total_score += 3
        player = opponent
    # win
    elif player_move == 'Z':
        total_score += 6
        player = losing_shapes[opponent]
    total_score += shape_scores[player]

print(total_score)
