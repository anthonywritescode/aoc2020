-- our puzzle input
CREATE TABLE input (value STRING);
INSERT INTO input VALUES (CAST(readfile('input.txt') AS TEXT));

CREATE TABLE input_n (card_n INT, door_n INT);
INSERT INTO input_n
SELECT
    CAST(SUBSTR(input.value, 1, INSTR(input.value, CHAR(10))) AS INT),
    CAST(SUBSTR(input.value, INSTR(input.value, CHAR(10))) AS INT)
FROM input;

CREATE TABLE door_loop_size (n INT);
WITH RECURSIVE
    nn (i, n)
AS (
    SELECT 0, 1
    UNION ALL
    SELECT nn.i + 1, nn.n * 7 % 20201227
    FROM nn
    WHERE nn.n != (SELECT input_n.door_n FROM input_n)
)
INSERT INTO door_loop_size
SELECT MAX(nn.i) FROM nn;

WITH RECURSIVE
    nn (i, n)
AS (
    SELECT 0, 1
    UNION ALL
    SELECT nn.i + 1, nn.n * (SELECT input_n.card_n FROM input_n) % 20201227
    FROM nn
    WHERE nn.i <= (SELECT door_loop_size.n FROM door_loop_size)
)
SELECT nn.n FROM nn WHERE nn.i = (SELECT door_loop_size.n FROM door_loop_size);
