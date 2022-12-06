# https://adventofcode.com/2022/day/6

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    buffer = file.read()


def first_occurence(num_chars):
    for i in range(0, len(buffer)-num_chars+1):
        curr = buffer[i:i+num_chars]
        if len(set(curr)) == num_chars:
            return i+num_chars

# Part 1
print(first_occurence(4))

# Part 2
print(first_occurence(14))