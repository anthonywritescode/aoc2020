import argparse
import collections
import os.path
from typing import Dict
from typing import List

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    prev_seen: Dict[int, List[int]] = collections.defaultdict(list)
    numbers = [int(n) for n in s.strip().split(',')]

    n = -1
    for turn in range(1, 2020 + 1):
        if turn <= len(numbers):
            n = numbers[turn - 1]
        elif len(prev_seen[n]) == 1:
            n = 0
        else:
            n = prev_seen[n][-1] - prev_seen[n][-2]

        prev_seen[n].append(turn)

    return n


INPUT_S = '''\
0,3,6
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 436),
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
