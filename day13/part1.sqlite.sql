-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE ts (value INT);
INSERT INTO ts
SELECT SUBSTR(input.value, 0, INSTR(input.value, char(10))) FROM input;

CREATE TABLE buses (bus INT);
WITH RECURSIVE
    nn (ROWID, n, rest)
AS (
    SELECT
        -1,
        '',
        (SELECT SUBSTR(input.value, INSTR(input.value, char(10)) + 1) FROM input)
    UNION ALL
    SELECT
        nn.ROWID + 1,
        CASE INSTR(nn.rest, ',')
            WHEN 0 THEN nn.rest
            ELSE SUBSTR(nn.rest, 0, INSTR(nn.rest, ','))
        END,
        CASE INSTR(nn.rest, ',')
            WHEN 0 THEN ''
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, ',') + 1)
        END
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
INSERT INTO buses (ROWID, bus)
SELECT nn.ROWID, nn.n FROM nn WHERE nn.n != '' AND nn.n != 'x';

SELECT bus * (
    (CAST((SELECT ts.value FROM ts) / bus AS INT) + 1) * bus -
    (SELECT ts.value FROM ts)
)
FROM buses
ORDER BY (CAST((SELECT ts.value FROM ts) / bus AS INT) + 1) * bus ASC
LIMIT 1;
