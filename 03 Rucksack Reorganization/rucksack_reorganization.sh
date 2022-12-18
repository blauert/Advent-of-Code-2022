#!/bin/bash
# https://adventofcode.com/2022/day/3

TMPFILE='/tmp/rr.py'

rm -f $TMPFILE

URL='https://raw.githubusercontent.com/blauert/Advent-of-Code-2022/master/03%20Rucksack%20Reorganization/rucksack_reorganization.py'

wget -O $TMPFILE $URL

echo 'Solution:'

python3 $TMPFILE

rm -f $TMPFILE