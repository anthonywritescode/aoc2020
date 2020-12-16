-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE buses (offset INT, bus INT);
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
INSERT INTO buses
SELECT nn.ROWID, nn.n FROM nn WHERE nn.n != '' AND nn.n != 'x';

WITH RECURSIVE
    nn (t, mult, buses_rowid)
AS (
    SELECT 0, (SELECT bus FROM buses WHERE offset = 0), 2
    UNION ALL
    SELECT
        CASE (
            (
                nn.t +
                (SELECT offset FROM buses WHERE ROWID = nn.buses_rowid)
            ) % (SELECT bus FROM buses WHERE ROWID = nn.buses_rowid)
        )
        WHEN 0 THEN nn.t
        ELSE nn.t + nn.mult
        END,
        CASE (
            (
                nn.t +
                (SELECT offset FROM buses WHERE ROWID = nn.buses_rowid)
            ) % (SELECT bus FROM buses WHERE ROWID = nn.buses_rowid)
        )
        WHEN 0 THEN nn.mult * (SELECT bus FROM buses WHERE ROWID = nn.buses_rowid)
        ELSE nn.mult
        END,
        CASE (
            (
                nn.t +
                (SELECT offset FROM buses WHERE ROWID = nn.buses_rowid)
            ) % (SELECT bus FROM buses WHERE ROWID = nn.buses_rowid)
        )
        WHEN 0 THEN nn.buses_rowid + 1
        ELSE nn.buses_rowid
        END
    FROM nn
    WHERE buses_rowid <= (SELECT MAX(ROWID) FROM buses)
)
SELECT MAX(t) FROM nn;
