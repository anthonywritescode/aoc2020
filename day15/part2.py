import argparse
import os.path
from typing import Dict

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    seen2: Dict[int, int] = {}
    seen1: Dict[int, int] = {}
    numbers = [int(n) for n in s.strip().split(',')]

    for turn in range(30_000_000):
        if turn < len(numbers):
            n = numbers[turn]
        elif n not in seen2:
            n = 0
        else:
            n = seen1[n] - seen2[n]

        if n in seen1:
            seen2[n] = seen1[n]
        seen1[n] = turn

    return n


INPUT_S = '''\
0,3,6
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 175594),
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
