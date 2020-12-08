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

CREATE TABLE answer(n INTEGER);
INSERT INTO answer VALUES(0);

CREATE TABLE pc(n INTEGER);
PRAGMA recursive_triggers = on;
CREATE TEMP TRIGGER ttrig
AFTER UPDATE OF n ON pc
WHEN (
    (SELECT COUNT(1) FROM visited WHERE visited.n = NEW.n) = 0 AND
    (SELECT COUNT(1) FROM prog) + 1 != NEW.n AND
    (SELECT answer.n FROM answer) = 0
)
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
        CASE NEW.n = (SELECT flip.n FROM flip ORDER BY ROWID DESC LIMIT 1)
        WHEN 0 THEN (
            CASE (SELECT prog.sym FROM prog WHERE ROWID = NEW.n)
            WHEN 'jmp' THEN (SELECT prog.val FROM prog WHERE ROWID = NEW.n)
            ELSE 1
            END
        ) ELSE (
            CASE (SELECT prog.sym FROM prog WHERE ROWID = NEW.n)
            WHEN 'nop' THEN (SELECT prog.val FROM prog WHERE ROWID = NEW.n)
            ELSE 1
            END
        )
        END
    );
END;

INSERT INTO pc VALUES (-1);

CREATE TABLE flip(n INTEGER);
CREATE TEMP TRIGGER fliptrig
AFTER INSERT ON flip
BEGIN
    DELETE FROM visited;
    UPDATE agg SET n = 0;
    UPDATE pc SET n = 0;

    INSERT INTO answer VALUES (
        CASE (SELECT pc.n FROM pc) = (SELECT COUNT(1) FROM prog) + 1
        WHEN 1 THEN (SELECT agg.n FROM agg)
        ELSE 0
        END
    );
END;

INSERT INTO flip
SELECT ROWID FROM prog
WHERE sym IN ('nop', 'jmp');

SELECT MAX(n) FROM answer;
