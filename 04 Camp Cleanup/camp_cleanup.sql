/*
https://adventofcode.com/2022/day/4

Usage: sqlite> .read camp_cleanup.sql
*/

DROP TABLE IF EXISTS aoc_input;

CREATE TABLE aoc_input (
	elf1_start INTEGER,
	elf1_end INTEGER,
	elf2_start INTEGER,
	elf2_end INTEGER
);

.mode csv

--.import test_input.csv aoc_input
.import real_input.csv aoc_input

-- For pretty output
.headers on
.mode column

WITH sections (contained, overlapping)
AS (
	SELECT
		CASE
			WHEN (elf1_start BETWEEN elf2_start AND elf2_end) AND (elf1_end BETWEEN elf2_start AND elf2_end)
				OR (elf2_start BETWEEN elf1_start AND elf1_end) AND (elf2_end BETWEEN elf1_start AND elf1_end)
				THEN 1
			ELSE 0
			END contained,
		CASE
			WHEN (elf2_start >= elf1_start AND elf2_start <= elf1_end) OR (elf1_start >= elf2_start AND elf1_start <= elf2_end)
				THEN 1
			ELSE 0
			END overlapping
	FROM aoc_input
	)
SELECT
sum(contained) AS part1,
sum(overlapping) AS part2
FROM sections;