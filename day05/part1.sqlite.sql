-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE lines (s STRING);
WITH RECURSIVE
    nn (s, rest)
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
INSERT INTO lines (s)
SELECT nn.s FROM nn;

CREATE TABLE ids (id INTEGER);
INSERT INTO ids
SELECT
    (CASE SUBSTR(s, 1, 1) WHEN 'B' THEN 512 ELSE 0 END) +
    (CASE SUBSTR(s, 2, 1) WHEN 'B' THEN 256 ELSE 0 END) +
    (CASE SUBSTR(s, 3, 1) WHEN 'B' THEN 128 ELSE 0 END) +
    (CASE SUBSTR(s, 4, 1) WHEN 'B' THEN 64 ELSE 0 END) +
    (CASE SUBSTR(s, 5, 1) WHEN 'B' THEN 32 ELSE 0 END) +
    (CASE SUBSTR(s, 6, 1) WHEN 'B' THEN 16 ELSE 0 END) +
    (CASE SUBSTR(s, 7, 1) WHEN 'B' THEN 8 ELSE 0 END) +
    (CASE SUBSTR(s, 8, 1) WHEN 'R' THEN 4 ELSE 0 END) +
    (CASE SUBSTR(s, 9, 1) WHEN 'R' THEN 2 ELSE 0 END) +
    (CASE SUBSTR(s, 10, 1) WHEN 'R' THEN 1 ELSE 0 END)
FROM lines;

SELECT MAX(id) FROM ids;
