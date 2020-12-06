-- our puzzle input
CREATE TABLE input (value TEXT);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

CREATE TABLE passports (grp INT, user INT, passport TEXT);
WITH RECURSIVE
    nn (grp, user, s, rest)
AS (
    SELECT
        0,
        0,
        (SELECT SUBSTR(input.value, 0, INSTR(input.value, char(10))) FROM input),
        (SELECT SUBSTR(input.value, INSTR(input.value, char(10)) + 1) FROM input)
    UNION ALL
    SELECT
        nn.grp + (SELECT INSTR(nn.rest, char(10)) = 1),
        nn.user + 1,
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
INSERT INTO passports
SELECT nn.grp, nn.user, nn.s FROM nn
WHERE LENGTH(nn.s) > 0;

CREATE TABLE grp_answers (
    grp INT,
    user INT,
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
    grp,
    user,
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
    (
        (SELECT SUM(a) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(b) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(c) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(d) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(e) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(f) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(g) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(h) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(i) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(j) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(k) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(l) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(m) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(n) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(o) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(p) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(q) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(r) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(s) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(t) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(u) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(v) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(w) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(x) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(y) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    ) +
    (
        (SELECT SUM(z) FROM grp_answers WHERE grp_answers.grp = tmp.grp) =
        (SELECT COUNT(1) FROM grp_answers WHERE grp_answers.grp = tmp.grp)
    )
)
FROM (SELECT DISTINCT grp FROM grp_answers) AS tmp;
