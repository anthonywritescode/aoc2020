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

CREATE TABLE parsed (s INT, e INT, c STRING, p STRING);
INSERT INTO parsed (s, e, c, p)
SELECT
    SUBSTR(s, 0, INSTR(s, '-')),
    SUBSTR(s, INSTR(s, '-') + 1, INSTR(s, ' ') - INSTR(s, '-') - 1),
    SUBSTR(s, INSTR(s, ' ') + 1, INSTR(s, ':') - INSTR(s, ' ') - 1),
    SUBSTR(s, INSTR(s, ':') + 1)
FROM lines;

SELECT COUNT(1)
FROM parsed
WHERE
    (
        SUBSTR(p, s + 1, 1) = c AND
        SUBSTR(p, e + 1, 1) != c
    ) OR (
        SUBSTR(p, s + 1, 1) != c AND
        SUBSTR(p, e + 1, 1) = c
    )
;
