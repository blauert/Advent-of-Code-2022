# https://adventofcode.com/2022/day/11

from math import lcm
from copy import deepcopy

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip().split() for line in file.readlines()]

observations = []

for i in range(len(lines)):
    if i % 7 == 0:
        # Monkey {monkey}:
        monkey = int(lines[i][-1].strip(':'))
        observations.append({})
    if (i-1) % 7 == 0:
        # Starting items: {items}
        observations[monkey]['items'] = [int(item.strip(',')) for item in lines[i][2:]]
    if (i-2) % 7 == 0:
        # Operation: new = old {operator} {operand}
        observations[monkey]['operator'] = lines[i][-2]
        observations[monkey]['operand'] = lines[i][-1]
    if (i-3) % 7 == 0:
        # Test: divisible by {divisor}
        observations[monkey]['divisor'] = int(lines[i][-1])
    if (i-4) % 7 == 0:
        # If true: throw to monkey {true_next}
        observations[monkey]['true_next'] = int(lines[i][-1])
    if (i-5) % 7 == 0:
        # If false: throw to monkey {false_next}
        observations[monkey]['false_next'] = int(lines[i][-1])


def worry_by_3(worry_level):
    # Worry level is divided by 3
    return worry_level // 3


def make_worry_func(monkeys):
    # Find least common multiple
    divisors = []
    for monkey in monkeys:
        divisors.append(monkey['divisor'])
    worry_lcm = lcm(*divisors)
    def worry_div(worry_level):
        # Keep worry level close to the least common multiple of divisors used by the monkeys
        if worry_level > (2*worry_lcm):
            worry_level -= ((worry_level // worry_lcm) - 1) * worry_lcm   
        return worry_level
    return worry_div


def throw_items_around(monkeys, rounds, worry_func):
    items_inspected = {i: 0 for i in range(len(monkeys))}

    for i in range(rounds):
        for curr_id, curr_monkey in enumerate(monkeys):
            for worry_level in curr_monkey['items']:
                # Monkey inspects an item
                items_inspected[curr_id] += 1
                # Worry level increases
                if curr_monkey['operand'] == 'old':
                    operand = worry_level
                else:
                    operand = int(curr_monkey['operand'])
                if curr_monkey['operator'] == '+':
                    worry_level += operand
                elif curr_monkey['operator'] == '*':
                    worry_level *= operand
                # Monkey gets bored with item.
                worry_level = worry_func(worry_level)
                # Division test
                if worry_level % curr_monkey['divisor'] == 0:
                    next_monkey = curr_monkey['true_next']
                else:
                    next_monkey = curr_monkey['false_next']
                # Item is thrown to next monkey
                monkeys[next_monkey]['items'].append(worry_level)
            # All items thrown
            curr_monkey['items'] = []

    return items_inspected


# Part 1

monkeys = deepcopy(observations)
inspections = sorted(throw_items_around(monkeys, 20, worry_by_3).values())
monkey_business = inspections[-1] * inspections[-2]
print(monkey_business)


# Part 2

monkeys = deepcopy(observations)
worry_func = make_worry_func(monkeys)
inspections = sorted(throw_items_around(monkeys, 10000, worry_func).values())
monkey_business = inspections[-1] * inspections[-2]
print(monkey_business)