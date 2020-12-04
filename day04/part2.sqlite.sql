-- our puzzle input
CREATE TABLE input (value TEXT);
INSERT INTO input VALUES (TRIM(readfile('input.txt'), char(10)));

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

CREATE TABLE passport_data (
    byr INT,
    iyr INT,
    eyr INT,
    hgt TEXT,
    hcl TEXT,
    ecl TEXT,
    pid TEXT
);

INSERT INTO passport_data
SELECT
    json_extract(tmp_json.d, '$.byr'),
    json_extract(tmp_json.d, '$.iyr'),
    json_extract(tmp_json.d, '$.eyr'),
    json_extract(tmp_json.d, '$.hgt'),
    json_extract(tmp_json.d, '$.hcl'),
    json_extract(tmp_json.d, '$.ecl'),
    json_extract(tmp_json.d, '$.pid')
FROM (
    SELECT
        '{"' ||
        REPLACE(
            REPLACE(
                REPLACE(passport, ' ', '", "'),
                ':', '":"'
            ),
            char(10), '", "'
        ) ||
        '"}' as d
    FROM passports
) AS tmp_json;

SELECT COUNT(1) FROM passport_data
WHERE
    byr IS NOT NULL AND
    iyr IS NOT NULL AND
    eyr IS NOT NULL AND
    hgt IS NOT NULL AND
    hcl IS NOT NULL AND
    ecl IS NOT NULL AND
    pid IS NOT NULL AND

    1920 <= byr AND
    byr <= 2002 AND

    2010 <= iyr AND
    iyr <= 2020 AND

    2020 <= eyr AND
    eyr <= 2030 AND

    (
        (
            hgt LIKE '%cm' AND
            150 <= CAST(SUBSTR(hgt, 0, LENGTH(hgt) - 1) AS INT) AND
            CAST(SUBSTR(hgt, 0, LENGTH(hgt) - 1) AS INT) <= 193
        ) OR (
            hgt LIKE '%in' AND
            59 <= CAST(SUBSTR(hgt, 0, LENGTH(hgt) - 1) AS INT) AND
            CAST(SUBSTR(hgt, 0, LENGTH(hgt) - 1) AS INT) <= 76
        )
    ) AND

    hcl GLOB '#[a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9]' AND

    ecl in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth') AND

    pid GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
;
