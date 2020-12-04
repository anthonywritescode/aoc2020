-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE lines (s STRING);
WITH RECURSIVE
    nn (ROWID, s, rest)
AS (
    SELECT
        0,
        (SELECT SUBSTR(input.value, 0, INSTR(input.value, char(10))) FROM input),
        (SELECT SUBSTR(input.value, INSTR(input.value, char(10)) + 1) FROM input)
    UNION ALL
    SELECT
        ROWID + 1,
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
INSERT INTO lines (ROWID, s)
SELECT nn.ROWID, nn.s FROM nn;

SELECT (
    SELECT SUM(SUBSTR(s, ((ROWID * 1) % LENGTH(s)) + 1, 1) = '#')
    FROM lines
) * (
    SELECT SUM(SUBSTR(s, ((ROWID * 3) % LENGTH(s)) + 1, 1) = '#')
    FROM lines
) * (
    SELECT SUM(SUBSTR(s, ((ROWID * 5) % LENGTH(s)) + 1, 1) = '#')
    FROM lines
) * (
    SELECT SUM(SUBSTR(s, ((ROWID * 7) % LENGTH(s)) + 1, 1) = '#')
    FROM lines
) * (
    SELECT SUM(SUBSTR(s, ((ROWID / 2) % LENGTH(s)) + 1, 1) = '#')
    FROM lines
    WHERE ROWID % 2 = 0
);
