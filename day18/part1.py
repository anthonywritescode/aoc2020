import argparse
import os.path
import re
from typing import Match

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PAREN_RE = re.compile(r'\(([^()]+)\)')


def compute_part(s: str) -> int:
    parts = s.split()
    n = int(parts[0])

    i = 1
    while i < len(parts):
        op = parts[i]
        val = int(parts[i + 1])

        if op == '+':
            n += val
        elif op == '*':
            n *= val
        else:
            raise AssertionError(n, op, val)

        i += 2
    return n


def compute_part_replace(match: Match[str]) -> str:
    return str(compute_part(match[1]))


def compute(s: str) -> int:
    total = 0

    for line in s.splitlines():
        while PAREN_RE.search(line):
            line = PAREN_RE.sub(compute_part_replace, line)

        total += compute_part(line)

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1 + 2 * 3 + 4 * 5 + 6', 71),
        ('2 * 3 + (4 * 5)', 26),
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
