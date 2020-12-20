import argparse
import os.path
from typing import FrozenSet
from typing import NamedTuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Tile(NamedTuple):
    tile_id: int
    edges: FrozenSet[str]
    back_edges: FrozenSet[str]


def compute(s: str) -> int:
    tiles = []
    for tile_s in s.strip().split('\n\n'):
        lines = tile_s.splitlines()
        tileid = int(lines[0].split()[1][:-1])
        edges_f = frozenset((
            lines[1],
            ''.join(line[-1] for line in lines[1:]),
            lines[-1][::-1],
            ''.join(line[0] for line in lines[1:])[::-1],
        ))
        back_edges_f = frozenset(edge[::-1] for edge in edges_f)
        tiles.append(Tile(tileid, edges_f, back_edges_f))

    corners = []
    for i, tile in enumerate(tiles):
        edges = set(tile.edges)
        for j, other in enumerate(tiles):
            if i == j:
                continue
            for edge in tuple(edges):
                if edge in other.edges | other.back_edges:
                    edges.discard(edge)
        if len(edges) == 2:
            corners.append(tile.tile_id)

    n = 1
    for corner in corners:
        n *= corner
    return n


INPUT_S = '''\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 20899048083289),
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
