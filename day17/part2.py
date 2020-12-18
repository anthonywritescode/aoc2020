import argparse
import collections
import os.path
from typing import Counter
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    space = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                space[(0, 0, y, x)] = c

    for _ in range(6):
        marked: Counter[Tuple[int, int, int, int]] = collections.Counter()

        for (w, z, y, x), c in space.items():
            for w_i in (-1, 0, 1):
                for z_i in (-1, 0, 1):
                    for y_i in (-1, 0, 1):
                        for x_i in (-1, 0, 1):
                            if w_i == z_i == y_i == x_i == 0:
                                continue
                            marked[(w + w_i, z + z_i, y + y_i, x + x_i)] += 1

        new_space = {}
        for k, v in marked.items():
            if v == 3:
                new_space[k] = '#'

        for k in space:
            if marked[k] in {2, 3}:
                new_space[k] = '#'

        space = new_space

    return len(space)


INPUT_S = '''\
.#.
..#
###
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 848),
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
