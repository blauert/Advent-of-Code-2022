# https://adventofcode.com/2022/day/12

import heapq

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]


def elev(char):
    # Calculate elevation
    if char == 'S':
        return ord('a')
    elif char == 'E':
        return ord('z')
    return ord(char)


def build_unweighted_graph(lines):
    """
    Allowed steps: Climb up 1 elevation, or any elevation down
    """
    graph = {}
    x_max = len(lines) - 1
    y_max = len(lines[0]) - 1

    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            graph[(x, y)] = []

            # Find start
            if char == 'S':
                start = (x, y)
            # Find finish
            elif char == 'E':
                finish = (x, y)

            # Look left
            if x > 0:
                if elev(lines[x-1][y]) - elev(char) <= 1:
                    graph[(x, y)].append((x-1, y))
            # Look right
            if x < x_max:
                if elev(lines[x+1][y]) - elev(char) <= 1:
                    graph[(x, y)].append((x+1, y))
            # Look up
            if y > 0:
                if elev(lines[x][y-1]) - elev(char) <= 1:
                    graph[(x, y)].append((x, y-1))
            # Look down
            if y < y_max:
                if elev(lines[x][y+1]) - elev(char) <= 1:
                    graph[(x, y)].append((x, y+1))

    return start, finish, graph


def dijkstra(start, finish, graph):
    costs = {node: float('inf') for node in graph.keys()}
    costs[start] = 0
    processed = set()
    min_costs = [(0, start)]

    while min_costs:
        curr_cost, curr = heapq.heappop(min_costs)
        if curr in processed:
            continue
        processed.add(curr)
        for neighbor in graph[curr]:
            if neighbor in processed:
                continue
            new_cost = curr_cost + 1  # Cost is 1 step regardless of elevation
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(min_costs, (new_cost, neighbor))
    return costs[finish]


# Part 1
start, finish, graph = build_unweighted_graph(lines)
print(dijkstra(start, finish, graph))


# Part 2
possible_starting_positions = []
for x, line in enumerate(lines):
    for y, char in enumerate(line):
        if char == 'a' or char == 'S':
            possible_starting_positions.append((x, y))
shortest_paths = []
for start in possible_starting_positions:
    heapq.heappush(shortest_paths, dijkstra(start, finish, graph))
print(shortest_paths[0])