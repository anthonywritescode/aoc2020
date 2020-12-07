-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE parents (parent TEXT, n INT, child TEXT);
WITH RECURSIVE
    nn (parent, n, child, rest)
AS (
    SELECT
        '',
        0,
        '',
        (SELECT value FROM input)
    UNION ALL
    SELECT
        CASE (
            (
                INSTR(nn.rest, ',') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, ',')
            ) AND (
                INSTR(nn.rest, '.') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, '.')
            )
        )
            WHEN 1 THEN SUBSTR(nn.rest, 0, INSTR(nn.rest, ' bags'))
            ELSE nn.parent
        END,
        CASE (
            (
                INSTR(nn.rest, ',') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, ',')
            ) AND (
                INSTR(nn.rest, '.') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, '.')
            )
        )
            WHEN 1 THEN
                CASE SUBSTR(nn.rest, INSTR(nn.rest, ' contain ') + 9) LIKE 'no other%'
                    WHEN 1 THEN 0
                    ELSE SUBSTR(nn.rest, INSTR(nn.rest, ' contain ') + 9, 1)
                END
            ELSE SUBSTR(nn.rest, 1, 1)
        END,
        CASE (
            (
                INSTR(nn.rest, ',') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, ',')
            ) AND (
                INSTR(nn.rest, '.') = 0 OR
                INSTR(nn.rest, ' contain ') < INSTR(nn.rest, '.')
            )
        )
            WHEN 1 THEN
                CASE SUBSTR(nn.rest, INSTR(nn.rest, ' contain ') + 9) LIKE 'no other%'
                    WHEN 1 THEN ''
                    ELSE SUBSTR(
                        nn.rest,
                        INSTR(nn.rest, ' contain ') + 11,
                        -1 + INSTR(
                            SUBSTR(
                                nn.rest,
                                INSTR(nn.rest, ' contain ') + 11
                            ),
                            ' bag'
                        )
                    )
                END
            ELSE SUBSTR(nn.rest, 3, INSTR(nn.rest, ' bag') - 3)
        END,
        CASE (
            INSTR(nn.rest, ',') > 0 AND
            INSTR(nn.rest, ',') < INSTR(nn.rest, '.')
        )
            WHEN 1 THEN SUBSTR(nn.rest, INSTR(nn.rest, ',') + 2)
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, '.') + 2)
        END
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
INSERT INTO parents (parent, n, child)
SELECT nn.parent, nn.n, nn.child
FROM nn WHERE nn.parent != '' AND nn.child != '';

CREATE TABLE counts (n);

CREATE TABLE stack (n, color);
PRAGMA recursive_triggers = on;
CREATE TEMP TRIGGER ttrig
AFTER INSERT ON stack
BEGIN
    INSERT INTO counts
    SELECT NEW.n WHERE NEW.color != 'shiny gold';

    INSERT INTO stack
    SELECT n * NEW.n, child FROM parents
    WHERE parent = NEW.color;
END;

INSERT INTO stack VALUES (1, 'shiny gold');

SELECT SUM(n) FROM counts;
