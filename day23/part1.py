import argparse
import collections
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    cups = collections.deque(int(n) for n in list(s.strip()))
    maximum = max(cups)

    for _ in range(100):
        current = cups[0]
        cups.rotate(-1)
        taken = [cups.popleft() for _ in range(3)]

        current_label = (current - 1)
        if current_label == 0:
            current_label = maximum
        while current_label in taken:
            current_label = (current_label - 1)
            if current_label == 0:
                current_label = maximum

        idx = cups.index(current_label)
        cups.rotate(-1 * idx - 1)
        cups.extend(taken)
        cups.rotate(idx + 3 + 1)

    cups.rotate(-cups.index(1))
    cups.popleft()
    return int(''.join(str(n) for n in cups))


INPUT_S = '''\
389125467
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 67384529),
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
