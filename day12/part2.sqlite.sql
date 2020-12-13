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

CREATE TABLE answer (n INT);
WITH RECURSIVE
    nn (ROWID, s_x, s_y, w_x, w_y)
AS (
    SELECT 1, 0, 0, 10, 1
    UNION ALL
    SELECT
        nn.ROWID + 1,

        -- s_x
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'F' THEN
            nn.s_x +
            nn.w_x *
            (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        ELSE nn.s_x
        END,
        -- s_y
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'F' THEN
            nn.s_y +
            nn.w_y *
            (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        ELSE nn.s_y
        END,
        -- w_x
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'E' THEN
            nn.w_x + (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'W' THEN
            nn.w_x - (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'L' THEN
            CASE (SELECT dirs.num / 90 % 4 FROM dirs WHERE dirs.ROWID = nn.ROWID)
                WHEN 0 THEN nn.w_x
                WHEN 1 THEN nn.w_y * -1
                WHEN 2 THEN nn.w_x * -1
                WHEN 3 THEN nn.w_y
                ELSE NULL
            END
        WHEN 'R' THEN
            CASE (SELECT dirs.num / 90 % 4 FROM dirs WHERE dirs.ROWID = nn.ROWID)
                WHEN 0 THEN nn.w_x
                WHEN 1 THEN nn.w_y
                WHEN 2 THEN nn.w_x * -1
                WHEN 3 THEN nn.w_y * -1
                ELSE NULL
            END
        ELSE nn.w_x
        END,
        -- w_y
        CASE (SELECT dirs.dir FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'N' THEN
            nn.w_y + (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'S' THEN
            nn.w_y - (SELECT dirs.num FROM dirs WHERE dirs.ROWID = nn.ROWID)
        WHEN 'L' THEN
            CASE (SELECT dirs.num / 90 % 4 FROM dirs WHERE dirs.ROWID = nn.ROWID)
                WHEN 0 THEN nn.w_y
                WHEN 1 THEN nn.w_x
                WHEN 2 THEN nn.w_y * -1
                WHEN 3 THEN nn.w_x * -1
                ELSE NULL
            END
        WHEN 'R' THEN
            CASE (SELECT dirs.num / 90 % 4 FROM dirs WHERE dirs.ROWID = nn.ROWID)
                WHEN 0 THEN nn.w_y
                WHEN 1 THEN nn.w_x * -1
                WHEN 2 THEN nn.w_y * -1
                WHEN 3 THEN nn.w_x
                ELSE NULL
            END
        ELSE nn.w_y
        END
    FROM nn
    WHERE nn.ROWID <= (SELECT COUNT(1) FROM dirs)
)
INSERT INTO answer
SELECT ABS(nn.s_x) + ABS(nn.s_y)
FROM nn
WHERE ROWID = (SELECT MAX(ROWID) FROM nn);

SELECT * FROM answer;
