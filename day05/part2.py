import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    possible = set(range(1024))

    for line in s.splitlines():
        line = line.replace('F', '0').replace('B', '1')
        line = line.replace('R', '1').replace('L', '0')
        possible.discard(int(line, 2))

    for candidate in possible:
        if candidate - 1 not in possible and candidate + 1 not in possible:
            return candidate
    else:
        raise NotImplementedError('unreachable')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
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
