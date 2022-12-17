#!/bin/bash

FILE=./real_input.txt
#FILE=./test_input.txt

TMPFILE=$(mktemp ./tmpcals.XXX)
control_c() {
    rm -f $TMPFILE
    exit
}
trap control_c SIGINT


# Count calories
cal_count=0
for line in $(cat $FILE); do
    curr_line=$(echo $line | tr -d '\r')  # This is super slow
    if [ $curr_line ]; then
        cal_count=$(expr $cal_count + $curr_line)
    else
        echo "Counting... $cal_count"
        echo $cal_count >> $TMPFILE
        cal_count=0
    fi
done
echo "Counting... $cal_count"
echo $cal_count >> $TMPFILE


# Part 1
largest=$(cat $TMPFILE | sort -n | tail -1)
echo "Part 1: $largest"


# Part 2
sum=0
three_largest=$(cat $TMPFILE | sort -n | tail -3)
for num in $three_largest; do
    sum=$(expr $sum + $num)
done
echo "Part 2: $sum"


# Clean up
rm -f $TMPFILE