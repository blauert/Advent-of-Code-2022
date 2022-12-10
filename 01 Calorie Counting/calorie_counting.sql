/*
https://adventofcode.com/2022/day/1

Usage: sqlite> .read calorie_counting.sql
*/

DROP TABLE IF EXISTS aoc_input;

CREATE TABLE aoc_input (
	elf TEXT,
	cals INTEGER
);

.mode csv

--.import test_input.csv aoc_input
.import real_input.csv aoc_input

-- For pretty output
.headers on
.mode column

DROP TABLE IF EXISTS parts;
CREATE TABLE parts (
	part TEXT
);

INSERT INTO parts (part) VALUES ('Part 1'), ('Part 2');

WITH
part1 (solution)
AS (
	WITH calories (total_cals)
	AS (
		SELECT sum(cals)
		FROM aoc_input
		GROUP BY elf
		)
	SELECT max(total_cals) AS solution
	FROM calories
	),
part2 (solution)
AS (
	WITH calories (top3)
	AS (
		SELECT sum(cals) AS total_cals
		FROM aoc_input
		GROUP BY elf
		ORDER BY total_cals DESC
		LIMIT 3
		)
	SELECT sum(top3) AS solution
	FROM calories
	)
SELECT *
FROM parts JOIN part1
ON parts.ROWID = 1
UNION
SELECT *
FROM parts JOIN part2
ON parts.ROWID = 2;