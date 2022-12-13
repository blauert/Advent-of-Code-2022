/*
https://adventofcode.com/2022/day/3

Usage: sqlite> .read rucksack_reorganization.sql
*/

DROP TABLE IF EXISTS aoc_input_1;
DROP TABLE IF EXISTS aoc_input_2;

-- For import
.mode csv

--.import test_input_1.csv aoc_input_1
--.import test_input_2.csv aoc_input_2
.import real_input_1.csv aoc_input_1
.import real_input_2.csv aoc_input_2
/*
aoc_input_1
rowid  comp1                            comp2
-----  -------------------------------  -------------------------------
1      v;J;r;w;p;W;t;w;J;g;W;r          h;c;s;F;M;M;f;F;F;h;F;p
2      j;q;H;R;N;q;R;j;q;z;j;G;D;L;G;L  r;s;F;M;f;F;Z;S;r;L;r;F;Z;s;S;L
3      P;m;m;d;z;q;P;r;V                v;P;w;w;T;W;B;w;g
---snip---

aoc_input_2
rowid  elf1                  elf2                  elf3
-----  ----------            ----------            ----------
1      v;J;r;w;p;---snip---  j;q;H;R;N;---snip---  P;m;m;d;z;---snip---
2      w;M;q;v;L;---snip---  t;t;g;J;t;---snip---  C;r;Z;s;J;---snip---
*/

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
INSERT INTO parts (part) VALUES ('Part 1'), ('Part 2');

WITH
part1 (solution)
AS (
    WITH priorities (prio)
    AS (
        WITH unique_items
        AS (
            WITH
            split_comp1(rowid, item, csv)
            AS (
                SELECT
                    ROWID,
                    -- https://stackoverflow.com/questions/24258878/how-to-split-comma-separated-values
                    -- in final WHERE, we filter raw csv (1st row) and terminal ';' (last row)
                    '', 
                    -- here you can SELECT FROM e.g. another table: col_name||';' FROM X
                    comp1||';' FROM aoc_input_1 -- terminate with ';' indicating csv ending
                -- 'recursive query'
                UNION ALL SELECT
                    rowid,
                    substr(csv, 0, instr(csv, ';')), -- each item contains text up to next ';'
                    substr(csv, instr(csv, ';') + 1) -- next recursion parses csv after this ';'
                FROM split_comp1 -- recurse
                WHERE csv != '' -- break recursion once no more csv words exist
                ),
            split_comp2(rowid, item, csv)
            AS (
                SELECT
                    ROWID, '', comp2||';' FROM aoc_input_1
                UNION ALL SELECT
                    rowid,
                    substr(csv, 0, instr(csv, ';')),
                    substr(csv, instr(csv, ';') + 1)
                FROM split_comp2
                WHERE csv != ''
                )
            SELECT
            split_comp1.rowid, split_comp1.item
            FROM split_comp1
            WHERE split_comp1.item!='' -- filter out 1st/last rows

            INTERSECT
            /*
            rowid  item
            -----  ----
            1      p
            2      L
            3      P
            4      v
            5      t
            6      s
            */

            SELECT
            split_comp2.rowid, split_comp2.item
            FROM split_comp2
            WHERE split_comp2.item!='' -- filter out 1st/last rows
            )
        SELECT
        CASE
            WHEN unicode(item) >= 97 THEN unicode(item) - 96 -- lowercase
            ELSE unicode(item) - 38 -- uppercase
            END AS priority
        /*
        priority
        --------
        16
        38
        42
        22
        20
        19
        */
        FROM unique_items
        )
    SELECT sum(prio)
    /*
    sum(prio)
    ---------
    157
    */
    FROM priorities
    ),
part2 (solution)
AS (
    WITH priorities (prio)
    AS (
        WITH unique_items
        AS (
            WITH
            split_elf1(rowid, item, csv)
            AS (
                SELECT
                    ROWID, '', elf1||';' FROM aoc_input_2
                UNION ALL SELECT
                    rowid,
                    substr(csv, 0, instr(csv, ';')),
                    substr(csv, instr(csv, ';') + 1)
                FROM split_elf1
                WHERE csv != ''
                ),
            split_elf2(rowid, item, csv)
            AS (
                SELECT
                    ROWID, '', elf2||';' FROM aoc_input_2
                UNION ALL SELECT
                    rowid,
                    substr(csv, 0, instr(csv, ';')),
                    substr(csv, instr(csv, ';') + 1)
                FROM split_elf2
                WHERE csv != ''
                ),
            split_elf3(rowid, item, csv)
            AS (
                SELECT
                    ROWID, '', elf3||';' FROM aoc_input_2
                UNION ALL SELECT
                    rowid,
                    substr(csv, 0, instr(csv, ';')),
                    substr(csv, instr(csv, ';') + 1)
                FROM split_elf3
                WHERE csv != ''
                )
            SELECT
            split_elf1.rowid, split_elf1.item
            FROM split_elf1
            WHERE split_elf1.item!=''

            INTERSECT

            SELECT
            split_elf2.rowid, split_elf2.item
            FROM split_elf2
            WHERE split_elf2.item!=''

            INTERSECT

            SELECT
            split_elf3.rowid, split_elf3.item
            FROM split_elf3
            WHERE split_elf3.item!=''
            )
        SELECT
        CASE
            WHEN unicode(item) >= 97 THEN unicode(item) - 96
            ELSE unicode(item) - 38
            END AS priority
        FROM unique_items
        )
    SELECT sum(prio)
    FROM priorities
	)
SELECT *
/*
part    solution
------  --------
Part 1  157
Part 2  70
*/
FROM parts JOIN part1
ON parts.ROWID = 1
UNION
SELECT *
FROM parts JOIN part2
ON parts.ROWID = 2;