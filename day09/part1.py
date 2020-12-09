import argparse
import itertools
import os.path
from typing import List

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, n: int = 25) -> int:
    seen: List[int] = []
    for i, line in enumerate(s.splitlines()):
        if i >= n:
            prev_25 = seen[-n:]
            for x, y in itertools.combinations(prev_25, 2):
                if x + y == int(line):
                    break
            else:
                return int(line)
        seen.append(int(line))
    raise NotImplementedError('unreachable')


INPUT_S = '''\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 127),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, n=5) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
