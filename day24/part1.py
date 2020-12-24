import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


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
        (INPUT_S, 10),
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
