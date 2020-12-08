-- our puzzle input
CREATE TABLE input (value TEXT);
INSERT INTO input VALUES (CAST(readfile('input.txt') AS TEXT));

CREATE TABLE prog (sym TEXT, val INTEGER);
WITH RECURSIVE
    nn (ROWID, sym, val, rest)
AS (
    SELECT -1, '', -1, (SELECT input.value FROM input)
    UNION ALL
    SELECT
        nn.ROWID + 1,
        SUBSTR(nn.rest, 0, INSTR(nn.rest, ' ')),
        0 + SUBSTR(
            nn.rest,
            INSTR(nn.rest, ' ') + 1,
            INSTR(nn.rest, char(10)) - INSTR(nn.rest, ' ') - 1
        ),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
INSERT INTO prog (ROWID, sym, val)
SELECT nn.ROWID, nn.sym, nn.val FROM nn WHERE ROWID >= 0;

CREATE TABLE agg(n INTEGER);
INSERT INTO agg VALUES (0);

CREATE TABLE visited(n INTEGER);

CREATE TABLE pc(n INTEGER);
PRAGMA recursive_triggers = on;
CREATE TEMP TRIGGER ttrig
AFTER UPDATE OF n ON pc
WHEN (SELECT COUNT(1) FROM visited WHERE visited.n = NEW.n) = 0
BEGIN
    INSERT INTO visited VALUES (NEW.n);

    UPDATE agg
    SET n = (SELECT agg.n FROM agg) + (
        CASE (SELECT prog.sym FROM prog WHERE ROWID = NEW.n)
        WHEN 'acc' THEN (SELECT prog.val FROM prog WHERE ROWID = NEW.n)
        ELSE 0
        END
    );

    UPDATE pc
    SET n = NEW.n + (
        CASE (SELECT prog.sym FROM prog WHERE ROWID = NEW.n)
        WHEN 'jmp' THEN (SELECT prog.val FROM prog WHERE ROWID = NEW.n)
        ELSE 1
        END
    );
END;

INSERT INTO pc VALUES (-1);
UPDATE pc SET n = 0;

SELECT * FROM agg;
