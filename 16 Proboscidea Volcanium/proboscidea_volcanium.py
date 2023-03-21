# https://adventofcode.com/2022/day/16

import re
from copy import deepcopy
from dataclasses import dataclass, field

INPUT_FILE = 'real_input.txt'
#INPUT_FILE = 'test_input.txt'

scan = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? ([A-Z]{2}(, [A-Z]{2})*)')

with open(INPUT_FILE) as file:
    SCANS = [[line[0], int(line[1]), line[2].split(", ")]
             for line in [scan.findall(line)[0] for line in file.readlines()]]

START_POSITION = 'AA'
TIME_LIMIT = 30

FLOW_RATES = {}
TUNNELS = {}

for valve in SCANS:
    FLOW_RATES[valve[0]] = valve[1]
    TUNNELS[valve[0]] = valve[2]


# Thanks ChatGPT
graph = TUNNELS

# Create a dictionary to hold the distances between each pair of nodes
distances = {}

# Initialize the distances between nodes that have an edge between them
for node1 in graph:
    for node2 in graph[node1]:
        distances[(node1, node2)] = 1

# Run the Floyd-Warshall algorithm to compute the shortest distance between all pairs of nodes
for k in graph:
    for i in graph:
        for j in graph:
            if (i, j) not in distances:
                distances[(i, j)] = float('inf')
            if (i, k) in distances and (k, j) in distances:
                distances[(i, j)] = min(distances[(i, j)], distances[(i, k)] + distances[(k, j)])

# Print the distances between each pair of nodes
#for node1 in graph:
#    for node2 in graph:
#        print(f"Distance between {node1} and {node2}: {distances.get((node1, node2), float('inf'))}")


@dataclass
class Path:
    valves_to_open: set
    curr_position: str = START_POSITION
    time_remaining: int = TIME_LIMIT
    released: int = 0
    potential: int = 0
    rooms_visited: set = field(default_factory=set)

    def __post_init__(self):
        # https://docs.python.org/3/library/dataclasses.html#post-init-processing
        self._calculate_potential()
    
    def _calculate_potential(self):
        # Used for pruning.
        potential = 0
        for valve in self.valves_to_open:
            if self.time_remaining > distances[(self.curr_position, valve)]:
                potential += (self.time_remaining - distances[(self.curr_position, valve)]) * FLOW_RATES[valve]
        self.potential = potential
    
    def _count_down(self):
        self._calculate_potential()
        self.time_remaining -= 1
    
    def walk_tunnel(self, new_position):
        self.curr_position = new_position
        self.rooms_visited.add(new_position)  # track visited to avoid running in circles
        self._count_down()

    def open_valve(self, valve):
        self.valves_to_open.remove(valve)
        self._count_down()
        self.released += (FLOW_RATES[valve] * self.time_remaining)
        self.rooms_visited = set(self.curr_position)  # reset visited rooms when opening a valve

    def to_tuple(self):
        return (self.curr_position, self.time_remaining, self.released)


def part1_slow():
    max_pressure = 0
    start = Path({valve for valve, rate in FLOW_RATES.items() if rate > 0})
    paths = [start]
    walked_paths = set()  # avoid walking the same path multiple times

    while paths:
        curr = paths.pop()
        walked_paths.add(curr.to_tuple())

        if (curr.released + curr.potential) > max_pressure:

            # open valve
            if curr.curr_position in curr.valves_to_open:
                new_path = deepcopy(curr)
                new_path.open_valve(curr.curr_position)
                if new_path.to_tuple() not in walked_paths:
                    paths.append(new_path)

                # new max pressure
                max_pressure = max(max_pressure, new_path.released)

            # walk tunnels
            for new_pos in TUNNELS[curr.curr_position]:
                if new_pos not in curr.rooms_visited:
                    new_path = deepcopy(curr)
                    new_path.walk_tunnel(new_pos)
                    if new_path.to_tuple() not in walked_paths:
                        paths.append(new_path)


    print(f"Part 1: {max_pressure}")


if __name__ == "__main__":
    part1_slow()