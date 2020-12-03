import argparse
from typing import List

import pytest

from support import timing


def _compute(lines: List[str], x_move: int, y_move: int) -> int:
    x, y = 0, 0

    count = 0
    x += x_move
    x %= len(lines[0])
    y += y_move
    while y < len(lines):
        if lines[y][x] == '#':
            count += 1
        x += x_move
        x %= len(lines[0])
        y += y_move

    return count


'''\
Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
'''


def compute(s: str) -> int:
    lines = s.splitlines()

    return (
        _compute(lines, 1, 1) *
        _compute(lines, 3, 1) *
        _compute(lines, 5, 1) *
        _compute(lines, 7, 1) *
        _compute(lines, 1, 2)
    )


INPUT = '''\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT, 336),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
