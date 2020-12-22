import argparse
import collections
import os.path
from typing import Deque

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    player1_s, player2_s = s.strip().split('\n\n')

    player1: Deque[int] = collections.deque()
    for line in player1_s.splitlines()[1:]:
        player1.append(int(line))
    player2: Deque[int] = collections.deque()
    for line in player2_s.splitlines()[1:]:
        player2.append(int(line))

    while player1 and player2:
        n1, n2 = player1.popleft(), player2.popleft()
        if n1 > n2:
            player1.extend((n1, n2))
        else:
            player2.extend((n2, n1))

    total = 0
    if player1:
        for i, el in enumerate(reversed(player1), 1):
            total += i * el
    else:
        for i, el in enumerate(reversed(player2), 1):
            total += i * el

    return total


INPUT_S = '''\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 306),
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
