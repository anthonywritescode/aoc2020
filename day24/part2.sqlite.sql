-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (CAST(readfile('input.txt') AS TEXT));

CREATE TABLE black (x INT, y INT);
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
INSERT INTO black
SELECT nn.x, nn.y FROM nn
WHERE nn.eol
GROUP BY nn.x, nn.y
HAVING COUNT(1) % 2 = 1;

CREATE TABLE counts (x INT, y INT, n INT);

CREATE TABLE iter (n INT);
PRAGMA recursive_triggers = on;
CREATE TEMP TRIGGER ttrig
AFTER UPDATE ON iter
WHEN NEW.n < 100
BEGIN
    DELETE FROM counts;

    INSERT INTO counts
    SELECT inner.x, inner.y, COUNT(1) FROM (
        SELECT black.x + 2 AS x, black.y AS y FROM black
        UNION ALL
        SELECT black.x - 2 AS x, black.y AS y FROM black
        UNION ALL
        SELECT black.x + 1 AS x, black.y + 2 AS y FROM black
        UNION ALL
        SELECT black.x - 1 AS x, black.y + 2 AS y FROM black
        UNION ALL
        SELECT black.x + 1 AS x, black.y - 2 AS y FROM black
        UNION ALL
        SELECT black.x - 1 AS x, black.y - 2 AS y FROM black
    ) AS inner
    GROUP BY inner.x, inner.y;

    DELETE FROM black
    WHERE
        (
            SELECT counts.n FROM counts
            WHERE counts.x = black.x AND counts.y = black.y
        ) IS NULL OR
        (
            SELECT counts.n FROM counts
            WHERE counts.x = black.x AND counts.y = black.y
        ) > 2
    ;

    INSERT INTO black
    SELECT x, y FROM counts
    WHERE
        n = 2 AND
        (
            SELECT COUNT(1) FROM black
            WHERE black.x = counts.x AND black.y = counts.y
        ) = 0;

    UPDATE iter SET n = NEW.n + 1;
END;

INSERT INTO iter VALUES (-1);
UPDATE iter SET n = 0;

SELECT COUNT(1) FROM black;
