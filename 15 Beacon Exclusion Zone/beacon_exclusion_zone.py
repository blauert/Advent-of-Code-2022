# https://adventofcode.com/2022/day/15

import re

INPUT_FILE = 'real_input.txt'
#INPUT_FILE = 'test_input.txt'

scan = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

with open(INPUT_FILE) as file:
    SCANS = [[(int(mo.group(1)), int(mo.group(2))), (int(mo.group(3)), int(mo.group(4)))]\
             for mo in [scan.search(line) for line in file.readlines()]]

if INPUT_FILE == 'test_input.txt':
    TARGET_ROW = 10
    MAX_XY = 20
elif INPUT_FILE == 'real_input.txt':
    TARGET_ROW = 2000000
    MAX_XY = 4000000


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def row_coverage(m_dist, target_dist):
    max_coverage = 2 * m_dist + 1
    return max_coverage - 2 * target_dist


def row_positions(x_center, row, number):
    positions = set()
    x_start = x_center - number // 2
    x_end = x_center + number // 2
    for x in range(x_start, x_end+1):
        positions.add((x, row))
    return positions


## Part 1

def part1():
    target_row_positions = set()
    beacons_in_target_row = set()

    for sensor, beacon in SCANS:
        covered_distance = manhattan_distance(sensor, beacon)
        target_distance = manhattan_distance(sensor, (sensor[0], TARGET_ROW))
        if beacon[1] == TARGET_ROW:
            beacons_in_target_row.add(beacon)
        if target_distance <= covered_distance:
            target_coverage = row_coverage(covered_distance, target_distance)
            covered = row_positions(sensor[0], TARGET_ROW, target_coverage)
            target_row_positions |= covered

    target_row_positions -= beacons_in_target_row

    print(f"Part 1: {len(target_row_positions)}")

part1()


## Part 2

