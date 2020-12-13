import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    s_y = 0
    s_x = 0
    w_y = 1
    w_x = 10

    lines = s.splitlines()
    for line in lines:
        d = line[0]
        n = int(line[1:])

        if d == 'N':
            w_y += n
        elif d == 'S':
            w_y -= n
        elif d == 'E':
            w_x += n
        elif d == 'W':
            w_x -= n
        elif d == 'L':
            for i in range(n // 90):
                w_y, w_x = w_x, w_y
                w_x *= -1
        elif d == 'R':
            for i in range(n // 90):
                w_y, w_x = w_x, w_y
                w_y *= -1
        elif d == 'F':
            s_y += w_y * n
            s_x += w_x * n
        else:
            raise NotImplementedError

    return abs(s_x) + abs(s_y)


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
        (SAMPLE, 286),
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
