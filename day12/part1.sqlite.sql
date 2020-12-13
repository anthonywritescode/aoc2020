-- our puzzle input
CREATE TABLE input (value TEXT);
INSERT INTO input VALUES (CAST(readfile('input.txt') AS TEXT));

CREATE TABLE dirs (dir TEXT, num INT);
WITH RECURSIVE
    nn (dir, num, rest)
AS (
    SELECT '', -1, (SELECT input.value FROM input)
    UNION ALL
    SELECT
        SUBSTR(nn.rest, 1, 1),
        CAST(SUBSTR(nn.rest, 2, INSTR(nn.rest, char(10)) - 1) AS INT),
        SUBSTR(nn.rest, INSTR(nn.rest, char(10)) + 1)
    FROM nn
    WHERE INSTR(nn.rest, char(10))
)
INSERT INTO dirs
SELECT nn.dir, nn.num FROM nn WHERE num >= 0;

CREATE TABLE vecs (d_x, d_y);
INSERT INTO vecs (ROWID, d_x, d_y) VALUES
    (0, 1, 0),
    (1, 0, -1),
    (2, -1, 0),
    (3, 0, 1);

CREATE TABLE answer (n INT);
WITH RECURSIVE
    nn (ROWID, s_x, s_y, dir_row)
AS (
    SELECT 1, 0, 0, 0
    UNION ALL
    SELECT
        nn.ROWID + 1,
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'E' THEN
            nn.s_x + (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'W' THEN
            nn.s_x - (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'F' THEN
            nn.s_x +
            (SELECT d_x FROM vecs WHERE vecs.ROWID = nn.dir_row) *
            (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        ELSE nn.s_x
        END,
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'N' THEN
            nn.s_y + (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'S' THEN
            nn.s_y - (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'F' THEN
            nn.s_y +
            (SELECT d_y FROM vecs WHERE vecs.ROWID = nn.dir_row) *
            (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        ELSE nn.s_y
        END,
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'R' THEN
            (
                nn.dir_row + 400 +
                (SELECT dirs.num / 90 FROM dirs WHERE dirs.ROWID = nn.ROWID)
            ) % 4
        WHEN 'L' THEN
            (
                nn.dir_row + 400 -
                (SELECT dirs.num / 90 FROM dirs WHERE dirs.ROWID = nn.ROWID)
            ) % 4
        ELSE nn.dir_row
        END
    FROM nn
    WHERE nn.ROWID <= (SELECT COUNT(1) FROM dirs)
)
INSERT INTO answer
SELECT ABS(nn.s_x) + ABS(nn.s_y)
FROM nn
WHERE ROWID = (SELECT MAX(ROWID) FROM nn);

SELECT * FROM answer;
