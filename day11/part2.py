import argparse
import collections
import os.path
from typing import Counter
from typing import Optional
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


"""\
If a seat is empty (L) and there are no occupied seats adjacent to it, the
seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also
occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
"""


def _index(lines: Tuple[str, ...], y: int, x: int) -> str:
    if y < 0:
        return ' '
    elif y >= len(lines):
        return ' '
    elif x < 0:
        return ' '
    elif x >= len(lines[0]):
        return ' '
    return lines[y][x]


def compute(s: str) -> int:
    lines = tuple(s.splitlines())

    prev: Optional[Tuple[str, ...]] = None
    while lines != prev:
        prev = lines

        dct: Counter[Tuple[int, int]] = collections.Counter()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    for d_y, d_x in (
                            (0, 1),
                            (0, -1),
                            (1, 0),
                            (-1, 0),
                            (1, 1),
                            (-1, -1),
                            (1, -1),
                            (-1, 1),
                    ):
                        y_i, x_i = y + d_y, x + d_x
                        c = _index(lines, y_i, x_i)
                        while c not in 'L# ':
                            y_i, x_i = y_i + d_y, x_i + d_x
                            c = _index(lines, y_i, x_i)
                        if c != ' ':
                            dct[(y_i, x_i)] += 1

        new_lines = []
        for y, line in enumerate(lines):
            line_c = []
            for x, c in enumerate(line):
                if c == 'L':
                    if dct[(y, x)] == 0:
                        line_c.append('#')
                    else:
                        line_c.append('L')
                elif c == '#':
                    if dct[(y, x)] >= 5:
                        line_c.append('L')
                    else:
                        line_c.append('#')
                else:
                    line_c.append(c)

            new_lines.append(''.join(line_c))

        lines = tuple(new_lines)

    return sum(line.count('#') for line in lines)


INPUT_S = '''\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 26),
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
