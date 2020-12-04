import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

"""\
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
"""
REQUIRED = frozenset(('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'))

"""\
byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
"""


def compute(s: str) -> int:
    count = 0
    for passport in s.split('\n\n'):
        fields_split = [s.strip().split(':', 1) for s in passport.split()]
        fields = {k: v for k, v in fields_split}
        if (
                fields.keys() >= REQUIRED and
                1920 <= int(fields['byr']) <= 2002 and
                2010 <= int(fields['iyr']) <= 2020 and
                2020 <= int(fields['eyr']) <= 2030 and
                (m1 := re.match(r'^(\d+)(cm|in)$', fields['hgt'])) and
                (
                    m1[2] == 'cm' and 150 <= int(m1[1]) <= 193 or
                    m1[2] == 'in' and 59 <= int(m1[1]) <= 76
                ) and
                re.match('^#[a-f0-9]{6}$', fields['hcl']) and
                fields['ecl'] in set('amb blu brn gry grn hzl oth'.split()) and
                re.match('^[0-9]{9}$', fields['pid'])
        ):
            count += 1
    return count


INPUT_S = '''\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 4),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
