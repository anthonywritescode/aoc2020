import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIV = 20201227


def get_loop_size(target: int) -> int:
    n = 1
    i = 0
    while n != target:
        n *= 7
        n %= 20201227
        i += 1
    return i


def transform(subject: int, loop: int) -> int:
    n = 1
    for _ in range(loop):
        n *= subject
        n %= 20201227
    return n


def compute(s: str) -> int:
    lines = s.strip().splitlines()
    card = int(lines[0])
    door = int(lines[1])
    return transform(card, get_loop_size(door))


INPUT_S = '''\
5764801
17807724
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 14897079),
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
