-- our puzzle input
CREATE TABLE input (value TEXT);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

-- DID NOT WORK FOR SOME REASON???
--
-- CREATE TEMP TRIGGER ttrig
-- AFTER UPDATE OF passport ON passports
-- BEGIN
--     WITH RECURSIVE
--         nn (s, rest)
--     AS (
--         SELECT
--             SUBSTR(NEW.value, 1, 1),
--             SUBSTR(NEW.value, 2)
--         UNION ALL
--         SELECT
--             SUBSTR(nn.rest, 1, 1),
--             SUBSTR(nn.rest, 2)
--         FROM nn
--         WHERE LENGTH(nn.rest) > 0
--     )
--     INSERT INTO grp_answers
--     SELECT NEW.ROWID, nn.s FROM nn;
-- END;

CREATE TABLE passports (passport TEXT);
WITH RECURSIVE
    nn (s, rest)
AS (
    SELECT
        (SELECT SUBSTR(input.value, 0, INSTR(input.value, char(10) || char(10))) FROM input),
        (SELECT SUBSTR(input.value, INSTR(input.value, char(10) || char(10)) + 2) FROM input)
    UNION ALL
    SELECT
        CASE INSTR(nn.rest, char(10) || char(10))
            WHEN 0 THEN nn.rest
            ELSE SUBSTR(nn.rest, 0, INSTR(nn.rest, char(10) || char(10)))
        END,
        CASE INSTR(nn.rest, char(10) || char(10))
            WHEN 0 THEN ''
            ELSE SUBSTR(nn.rest, INSTR(nn.rest, char(10) || char(10)) + 2)
        END
    FROM nn
    WHERE LENGTH(nn.rest) > 0
)
INSERT INTO passports (passport)
SELECT nn.s FROM nn;

CREATE TABLE grp_answers (
    grp INT,
    a BIT,
    b BIT,
    c BIT,
    d BIT,
    e BIT,
    f BIT,
    g BIT,
    h BIT,
    i BIT,
    j BIT,
    k BIT,
    l BIT,
    m BIT,
    n BIT,
    o BIT,
    p BIT,
    q BIT,
    r BIT,
    s BIT,
    t BIT,
    u BIT,
    v BIT,
    w BIT,
    x BIT,
    y BIT,
    z BIT
);
INSERT INTO grp_answers
SELECT
    ROWID,
    INSTR(passport, 'a') > 0,
    INSTR(passport, 'b') > 0,
    INSTR(passport, 'c') > 0,
    INSTR(passport, 'd') > 0,
    INSTR(passport, 'e') > 0,
    INSTR(passport, 'f') > 0,
    INSTR(passport, 'g') > 0,
    INSTR(passport, 'h') > 0,
    INSTR(passport, 'i') > 0,
    INSTR(passport, 'j') > 0,
    INSTR(passport, 'k') > 0,
    INSTR(passport, 'l') > 0,
    INSTR(passport, 'm') > 0,
    INSTR(passport, 'n') > 0,
    INSTR(passport, 'o') > 0,
    INSTR(passport, 'p') > 0,
    INSTR(passport, 'q') > 0,
    INSTR(passport, 'r') > 0,
    INSTR(passport, 's') > 0,
    INSTR(passport, 't') > 0,
    INSTR(passport, 'u') > 0,
    INSTR(passport, 'v') > 0,
    INSTR(passport, 'w') > 0,
    INSTR(passport, 'x') > 0,
    INSTR(passport, 'y') > 0,
    INSTR(passport, 'z') > 0
FROM passports;

SELECT SUM(
    a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q +
    r + s + t + u + v + w + x + y + z
)
FROM grp_answers;
