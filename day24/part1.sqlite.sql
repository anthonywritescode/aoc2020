-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (CAST(readfile('input.txt') AS TEXT));

WITH RECURSIVE
    nn (x, y, eol, rest)
AS (
    SELECT 0, 0, 0, (SELECT input.value FROM input)
    UNION ALL
    SELECT
        CASE nn.eol
        WHEN 1 THEN 0
        ELSE
            CASE SUBSTR(nn.rest, 1, 1)
            WHEN 'e' THEN nn.x + 2
            WHEN 'w' THEN nn.x - 2
            WHEN char(10) THEN nn.x
            ELSE
                CASE SUBSTR(nn.rest, 1, 2)
                WHEN 'ne' THEN nn.x + 1
                WHEN 'nw' THEN nn.x - 1
                WHEN 'se' THEN nn.x + 1
                WHEN 'sw' THEN nn.x - 1
                ELSE -1
                END
            END
        END,

        CASE nn.eol
        WHEN 1 THEN 0
        ELSE
            CASE SUBSTR(nn.rest, 1, 2)
            WHEN 'ne' THEN nn.y + 2
            WHEN 'nw' THEN nn.y + 2
            WHEN 'se' THEN nn.y - 2
            WHEN 'sw' THEN nn.y - 2
            ELSE nn.y
            END
        END,

        CASE nn.eol
        WHEN 1 THEN 0
        ELSE
            CASE SUBSTR(nn.rest, 1, 1)
            WHEN char(10) THEN 1
            ELSE 0
            END
        END,

        CASE nn.eol
        WHEN 1 THEN nn.rest
        ELSE
            CASE SUBSTR(nn.rest, 1, 1)
            WHEN 'e' THEN SUBSTR(nn.rest, 2)
            WHEN 'w' THEN SUBSTR(nn.rest, 2)
            WHEN char(10) THEN SUBSTR(nn.rest, 2)
            ELSE
                CASE SUBSTR(nn.rest, 1, 2)
                WHEN 'ne' THEN SUBSTR(nn.rest, 3)
                WHEN 'nw' THEN SUBSTR(nn.rest, 3)
                WHEN 'se' THEN SUBSTR(nn.rest, 3)
                WHEN 'sw' THEN SUBSTR(nn.rest, 3)
                ELSE -1
                END
            END
        END
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
SELECT COUNT(1) FROM (
    SELECT nn.x, nn.y, COUNT(1) FROM nn
    WHERE nn.eol
    GROUP BY nn.x, nn.y
    HAVING COUNT(1) % 2 = 1
);
