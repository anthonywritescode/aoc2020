-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE numbers (n INT);
INSERT INTO numbers (ROWID, n) VALUES (0, 0);
WITH RECURSIVE
    nn (n, rest)
AS (
    SELECT
        (SELECT SUBSTR(input.value, 0, INSTR(input.value, char(10))) FROM input),
        (SELECT SUBSTR(input.value, INSTR(input.value, char(10)) + 1) FROM input)
    UNION ALL
    SELECT
        CASE INSTR(nn.rest, char(10))
            WHEN 0 THEN nn.rest
            ELSE SUBSTR(nn.rest, 0, INSTR(nn.rest, char(10)))
        END,
        CASE INSTR(nn.rest, char(10))
            WHEN 0 THEN ''
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
        END
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
INSERT INTO numbers (n)
SELECT nn.n FROM nn ORDER BY CAST(nn.n AS INT) ASC;

CREATE TABLE n_for_streak (n, result);
WITH RECURSIVE
    nn (n, result, prev, prevprev)
AS (
    SELECT 1, 1, 0, 0
    UNION ALL
    SELECT
        nn.n + 1,
        nn.result + nn.prev + nn.prevprev,
        nn.result,
        nn.prev
    FROM nn
    WHERE nn.n < (SELECT COUNT(1) FROM numbers)
)
INSERT INTO n_for_streak SELECT nn.n, nn.result FROM nn;

WITH RECURSIVE
    nn (ROWID, n, comb, streak)
AS (
    SELECT -1, -2, 1, 1
    UNION ALL
    SELECT
        nn.ROWID + 1,
        (SELECT numbers.n FROM numbers WHERE numbers.ROWID = nn.ROWID + 1),
        CASE
            nn.n + 1 != (
                SELECT numbers.n
                FROM numbers WHERE numbers.ROWID = nn.ROWID + 1
            )
        WHEN 1 THEN nn.comb * (
            SELECT n_for_streak.result
            FROM n_for_streak
            WHERE n_for_streak.n = nn.streak
        )
        ELSE nn.comb
        END,
        CASE
            nn.n + 1 != (
                SELECT numbers.n
                FROM numbers WHERE numbers.ROWID = nn.ROWID + 1
            )
        WHEN 1 THEN 1
        ELSE nn.streak + 1
        END
    FROM nn
    WHERE nn.ROWID + 1 < (SELECT COUNT(1) FROM numbers)
)
SELECT
   comb * (
       SELECT n_for_streak.result
       FROM n_for_streak
       WHERE n_for_streak.n = streak
    )
FROM nn
WHERE ROWID = (SELECT MAX(ROWID) FROM nn);
