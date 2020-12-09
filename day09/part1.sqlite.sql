-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE numbers (n INT);
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
INSERT INTO numbers
SELECT nn.n FROM nn;

SELECT n FROM numbers
WHERE
    ROWID > 25 AND
    0 = (
        SELECT COUNT(1)
        FROM numbers AS numbers_inner
        INNER JOIN numbers AS numbers_inner2
        ON numbers_inner.ROWID != numbers_inner2.ROWID AND (
            numbers_inner2.ROWID >= numbers.ROWID - 25 AND
            numbers_inner2.ROWID < numbers.ROWID
        )
        WHERE numbers_inner.n + numbers_inner2.n = numbers.n AND (
            numbers_inner.ROWID >= numbers.ROWID - 25 AND
            numbers_inner.ROWID < numbers.ROWID
        )
    )
;
