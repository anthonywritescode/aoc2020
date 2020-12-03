import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    lines = s.splitlines()
    x, y = 0, 0

    count = 0
    x += 3
    x %= len(lines[0])
    y += 1
    while y < len(lines):
        if lines[y][x] == '#':
            count += 1
        x += 3
        x %= len(lines[0])
        y += 1

    return count


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
        (INPUT, 7),
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
