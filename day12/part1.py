import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


DIRECTIONS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]


def compute(s: str) -> int:
    x = 0
    y = 0
    direction = (0, 1)

    lines = s.splitlines()
    for line in lines:
        d = line[0]
        n = int(line[1:])

        if d == 'N':
            y -= n
        elif d == 'S':
            y += n
        elif d == 'E':
            x += n
        elif d == 'W':
            x -= n
        elif d == 'L':
            rotations = n // 90
            ind = DIRECTIONS.index(direction)
            direction = DIRECTIONS[(ind - rotations) % 4]
        elif d == 'R':
            rotations = n // 90
            ind = DIRECTIONS.index(direction)
            direction = DIRECTIONS[(ind + rotations) % 4]
        elif d == 'F':
            y += n * direction[0]
            x += n * direction[1]
        else:
            raise NotImplementedError

    return abs(x) + abs(y)


SAMPLE = '''\
F10
N3
F7
R90
F11
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SAMPLE, 25),
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
