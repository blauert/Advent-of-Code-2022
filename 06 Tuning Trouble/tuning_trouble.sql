/*
https://adventofcode.com/2022/day/6

Usage: sqlite> .read tuning_trouble.sql
*/

DROP TABLE IF EXISTS aoc_input;
CREATE TABLE aoc_input (
	signal TEXT
);

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
	WITH distinct_chars (id, char)
	AS (
		WITH
		chars (id, c1, c2, c3, c4)
		AS (
			WITH windows (id, win)
			AS (
				SELECT ROWID, group_concat(signal, '') OVER (
					ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
					) AS group_concat
				FROM aoc_input
				)
			SELECT id, substr(win, 1, 1), substr(win, 2, 1), substr(win, 3, 1), substr(win, 4, 1)
			FROM windows
			WHERE id > 3
			)
		SELECT id, c1
		FROM chars
		UNION
		SELECT id, c2
		FROM chars
		UNION
		SELECT id, c3
		FROM chars
		UNION
		SELECT id, c4
		FROM chars
		)
	SELECT id
	FROM distinct_chars
	GROUP BY id
	HAVING count(id) = 4
	LIMIT 1
	),
part2 (solution)
AS (
	WITH distinct_chars (id, char)
	AS (
		WITH
		chars (id, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14)
		AS (
			WITH windows (id, win)
			AS (
				SELECT ROWID, group_concat(signal, '') OVER (
					ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
					) AS group_concat
				FROM aoc_input
				)
			SELECT id, substr(win, 1, 1), substr(win, 2, 1), substr(win, 3, 1), substr(win, 4, 1),
					substr(win, 5, 1), substr(win, 6, 1), substr(win, 7, 1), substr(win, 8, 1),
					substr(win, 9, 1), substr(win, 10, 1), substr(win, 11, 1),
					substr(win, 12, 1), substr(win, 13, 1), substr(win, 14, 1)
			FROM windows
			WHERE id > 13
			)
		SELECT id, c1
		FROM chars
		UNION
		SELECT id, c2
		FROM chars
		UNION
		SELECT id, c3
		FROM chars
		UNION
		SELECT id, c4
		FROM chars
		UNION
		SELECT id, c5
		FROM chars
		UNION
		SELECT id, c6
		FROM chars
		UNION
		SELECT id, c7
		FROM chars
		UNION
		SELECT id, c8
		FROM chars
		UNION
		SELECT id, c9
		FROM chars
		UNION
		SELECT id, c10
		FROM chars
		UNION
		SELECT id, c11
		FROM chars
		UNION
		SELECT id, c12
		FROM chars
		UNION
		SELECT id, c13
		FROM chars
		UNION
		SELECT id, c14
		FROM chars
		)
	SELECT id
	FROM distinct_chars
	GROUP BY id
	HAVING count(id) = 14
	LIMIT 1
	)
SELECT *
FROM parts JOIN part1
ON parts.ROWID = 1
UNION
SELECT *
FROM parts JOIN part2
ON parts.ROWID = 2;