import argparse
import collections
import os.path
from typing import Counter
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


DIRECTIONS = [
    (2, 0),
    (-2, 0),
    (1, 2),
    (-1, 2),
    (1, -2),
    (-1, -2)
]


def compute(s: str) -> int:
    black_tiles = set()

    for line in s.strip().splitlines():
        x = y = i = 0
        while i < len(line):
            if line.startswith('e', i):
                x += 2
                i += 1
            elif line.startswith('w', i):
                x += -2
                i += 1
            elif line.startswith('ne', i):
                x += 1
                y += 2
                i += 2
            elif line.startswith('nw', i):
                x += -1
                y += 2
                i += 2
            elif line.startswith('se', i):
                x += 1
                y += -2
                i += 2
            elif line.startswith('sw', i):
                x += -1
                y += -2
                i += 2
            else:
                raise AssertionError(line[i:])

        if (x, y) in black_tiles:
            black_tiles.discard((x, y))
        else:
            black_tiles.add((x, y))

    for _ in range(100):
        counts: Counter[Tuple[int, int]] = collections.Counter()
        for x, y in black_tiles:
            for dx, dy in DIRECTIONS:
                counts[(x + dx, y + dy)] += 1

        to_discard = set()
        for x, y in black_tiles:
            if counts[(x, y)] == 0 or counts[(x, y)] > 2:
                to_discard.add((x, y))

        to_add = set()
        for (x, y), count in counts.items():
            if count == 2 and (x, y) not in black_tiles:
                to_add.add((x, y))

        black_tiles -= to_discard
        black_tiles |= to_add

    return len(black_tiles)


INPUT_S = '''\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 2208),
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
