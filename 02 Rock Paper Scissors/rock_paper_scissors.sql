/*
https://adventofcode.com/2022/day/2

Usage: sqlite> .read rock_paper_scissors.sql
*/

DROP TABLE IF EXISTS aoc_input;

CREATE TABLE aoc_input (
/*
opp  player
---  ------
A    Y
B    X
C    Z
*/
	opp TEXT,
	player TEXT
);

-- For import
.mode csv
.separator ' '

--.import test_input.txt aoc_input
.import real_input.txt aoc_input

-- For pretty output
.headers on
.mode column

DROP TABLE IF EXISTS parts;
CREATE TABLE parts (
/*
part
------
Part 1
Part 2
*/
	part TEXT
);
INSERT INTO parts (part)
VALUES ('Part 1'), ('Part 2');

DROP TABLE IF EXISTS shape_codes;
CREATE TABLE shape_codes (
/*
opp_code  player_code  shape
--------  -----------  -----
A         X            R
B         Y            P
C         Z            S
*/
	opp_code TEXT UNIQUE,  -- autoindexed
    player_code TEXT UNIQUE,  -- autoindexed
    shape TEXT
);
INSERT INTO shape_codes (opp_code, player_code, shape)
VALUES ('A', 'X', 'R'), ('B', 'Y', 'P'), ('C', 'Z', 'S');

DROP TABLE IF EXISTS shape_scores;
CREATE TABLE shape_scores (
/*
shape  score
-----  -----
R      1
P      2
S      3
*/
	shape TEXT UNIQUE,  -- autoindexed
    score INTEGER
);
INSERT INTO shape_scores (shape, score)
VALUES ('R', 1), ('P', 2), ('S', 3);

DROP TABLE IF EXISTS pairings;
CREATE TABLE pairings (
/*
winner  loser
------  -----
R       S
P       R
S       P
*/
	winner TEXT UNIQUE,  -- autoindexed
    loser TEXT UNIQUE  -- autoindexed
);
INSERT INTO pairings (winner, loser)
VALUES ('R', 'S'), ('P', 'R'), ('S', 'P');

WITH
part1 (solution)
AS (
	WITH scores
	AS (
		WITH game (opp, player)
		AS (
			SELECT shp1.shape AS opp_shape, shp2.shape AS player_shape
			/*
			opp_shape  player_shape
			---------  ------------
			R          P
			P          R
			S          S
			*/
			FROM aoc_input
			JOIN shape_codes AS shp1
			ON opp = shp1.opp_code
			JOIN shape_codes AS shp2
			ON player = shp2.player_code
			)
		SELECT opp, player, winner, score AS shape_score,
			CASE
				WHEN player = winner THEN score + 6
				WHEN player = opp THEN score + 3
				ELSE score
				END total_score
		/*
		opp  player  winner  shape_score  total_score
		---  ------  ------  -----------  -----------
		R    P       P       2            8
		P    R       S       1            1
		S    S       R       3            6
		*/
		FROM game
		JOIN shape_scores
		ON player = shape
		JOIN pairings
		ON opp = loser
		)
	SELECT sum(total_score)
	/*
	sum(total_score)
	----------------
	15
	*/
	FROM scores
	),
part2 (solution)
AS (
	WITH scores
	AS (
		WITH game (opp, outcome)
		AS (
			SELECT shape_codes.shape AS opp, player
			/*
			opp  player
			---  ------
			R    Y
			P    X
			S    Z
			*/
			FROM aoc_input
			JOIN shape_codes
			ON opp = shape_codes.opp_code
			)
		SELECT --opp,
			--pwin.winner AS winner,
			--plose.loser AS loser,
			--outcome,
			CASE
				WHEN outcome = 'X' THEN plose.loser
				WHEN outcome = 'Y' THEN opp
				WHEN outcome = 'Z' THEN pwin.winner
				END player,
			score AS shape_score,
			CASE
				WHEN outcome = 'X' THEN 0
				WHEN outcome = 'Y' THEN 3
				WHEN outcome = 'Z' THEN 6
				END round_score
		/*
		player  shape_score  round_score
		------  -----------  -----------
		R       1            3
		R       1            0
		R       1            6
		*/
		FROM game
		JOIN pairings AS pwin
		ON opp = pwin.loser
		JOIN pairings AS plose
		ON opp = plose.winner
		JOIN shape_scores
		ON player = shape
		)
	SELECT sum(shape_score + round_score)
	/*
	sum(shape_score + round_score)
	------------------------------
	12
	*/
	FROM scores
	)
SELECT *
/*
part    solution
------  --------
Part 1  15
Part 2  12
*/
FROM parts JOIN part1
ON parts.ROWID = 1
UNION
SELECT *
FROM parts JOIN part2
ON parts.ROWID = 2;