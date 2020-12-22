import argparse
import collections
import itertools
import os.path
from typing import Deque
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


# bool: player1 wins


def play_game(
        player1: Deque[int],
        player2: Deque[int],
) -> Tuple[bool, Deque[int]]:
    seen = set()

    while True:
        if player1 and not player2:
            return True, player1
        elif player2 and not player1:
            return False, player2

        gamestate = (tuple(player1), tuple(player2))
        if gamestate in seen:
            return True, player1

        c1, c2 = player1.popleft(), player2.popleft()
        if c1 <= len(player1) and c2 <= len(player2):
            sub_p1 = collections.deque(itertools.islice(player1, c1))
            sub_p2 = collections.deque(itertools.islice(player2, c2))
            player1_won, _ = play_game(sub_p1, sub_p2)
            if player1_won:
                player1.extend((c1, c2))
            else:
                player2.extend((c2, c1))
        elif c1 > c2:
            player1.extend((c1, c2))
        else:
            player2.extend((c2, c1))

        seen.add(gamestate)


def compute(s: str) -> int:
    player1_s, player2_s = s.strip().split('\n\n')

    player1: Deque[int] = collections.deque()
    for line in player1_s.splitlines()[1:]:
        player1.append(int(line))
    player2: Deque[int] = collections.deque()
    for line in player2_s.splitlines()[1:]:
        player2.append(int(line))

    _, result = play_game(player1, player2)

    total = 0
    for i, el in enumerate(reversed(result), 1):
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
        (INPUT_S, 291),
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
