#!/bin/bash

echo "Better use C:"
make | awk '{print $3}'
echo

echo "Or Python:"
python3 ./calorie_counting.py
echo

echo "Or even SQLite:"
echo ".read calorie_counting.sql" | sqlite3 | grep Part | awk '{print $3}'