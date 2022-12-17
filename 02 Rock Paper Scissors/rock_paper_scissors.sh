#!/bin/bash
# https://adventofcode.com/2022/day/2

FILE=./real_input.txt
#FILE=./test_input.txt

# Part 1

total_score_part1=0
count=0

for game in $(cat $FILE | sed -e 's/A/R/g' -e 's/B/P/g' -e 's/C/S/g' -e 's/X/R/g' -e 's/Y/P/g' -e 's/Z/S/g' -e 's/ //g'); do
    count=$(expr $count + 1)
    echo "Part 1: Processing... $count"
    op=$(echo $game | tr -d '\r')
    case $op in
        RP|PS|SR)
            total_score_part1=$(expr $total_score_part1 + 6)
            ;;
        RR|PP|SS)
            total_score_part1=$(expr $total_score_part1 + 3)
            ;;
    esac
    p=$(echo $op | cut -c 2)
    case $p in
        R)
            total_score_part1=$(expr $total_score_part1 + 1)
            ;;
        P)
            total_score_part1=$(expr $total_score_part1 + 2)
            ;;
        S)
            total_score_part1=$(expr $total_score_part1 + 3)
            ;;
    esac
done

# Part 2

total_score_part2=0
count=0

for game in $(cat $FILE | sed -e 's/A/R/g' -e 's/B/P/g' -e 's/C/S/g' -e 's/ //g'); do
    count=$(expr $count + 1)
    echo "Part 2: Processing... $count"
    op=$(echo $game | tr -d '\r')
    case $op in
        RY|PX|SZ)
            total_score_part2=$(expr $total_score_part2 + 1) # R
            ;;
        RZ|PY|SX)
            total_score_part2=$(expr $total_score_part2 + 2) # P
            ;;
        RX|PZ|SY)
            total_score_part2=$(expr $total_score_part2 + 3) # S
            ;;
    esac
    p=$(echo $op | cut -c 2)
    case $p in
        Z)
            total_score_part2=$(expr $total_score_part2 + 6)
            ;;
        Y)
            total_score_part2=$(expr $total_score_part2 + 3)
            ;;
    esac
done

# Solutions
echo "Part 1: $total_score_part1"
echo "Part 2: $total_score_part2"