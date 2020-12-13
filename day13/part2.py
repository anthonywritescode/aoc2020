import argparse
import os.path

import pytest
from sympy.ntheory.modular import crt

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    parsed = [
        (int(s), i)
        for i, s in enumerate(lines[1].split(','))
        if s != 'x'
    ]
    busses = [pt[0] for pt in parsed]
    mods = [-1 * pt[1] for pt in parsed]

    return crt(busses, mods)[0]


INPUT_S = '''\
939
7,13,x,x,59,x,31,19
'''
INPUT2_S = '''\
...
17,x,13,19
'''
INPUT3_S = '''\
...
67,7,59,61
'''
INPUT4_S = '''\
...
67,x,7,59,61
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1068781),
        (INPUT2_S, 3417),
        (INPUT3_S, 754018),
        (INPUT4_S, 779210),
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
