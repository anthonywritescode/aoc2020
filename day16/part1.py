import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

FIELD_RE = re.compile(r'^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$')


def compute(s: str) -> int:
    fields, my_ticket, nearby = s.split('\n\n')

    field_ranges = {}
    for line in fields.splitlines():
        m = FIELD_RE.match(line)
        assert m
        field_ranges[m[1]] = (int(m[2]), int(m[3]), int(m[4]), int(m[5]))

    invalid = 0
    for line in nearby.splitlines()[1:]:
        for n_s in line.split(','):
            n = int(n_s)
            for b1, e1, b2, e2 in field_ranges.values():
                if b1 <= n <= e1 or b2 <= n <= e2:
                    break
            else:
                invalid += n

    return invalid


INPUT_S = '''\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 71),
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
