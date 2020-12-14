import argparse
import collections
import os.path
import re
from typing import Generator
from typing import NamedTuple
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MEM_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')


class Mask(NamedTuple):
    ones_mask: int
    x_masks: Tuple[Tuple[int, int], ...]

    def targets(self, number: int) -> Generator[int, None, None]:
        number = number | self.ones_mask
        for x_mask_or, x_mask_and in self.x_masks:
            yield (number | x_mask_or) & x_mask_and


def parse_mask(s: str) -> Mask:
    one_mask = int(s.replace('X', '0'), 2)
    xs = [match.start() for match in re.finditer('X', s)]
    x_masks = []
    for i in range(1 << len(xs)):
        number_or = 0
        number_and = -1
        for j in range(len(xs)):
            bit = (i & (1 << j)) >> j
            if bit:
                number_or |= 1 << (len(s) - 1 - xs[j])
            else:
                number_and &= ~(1 << (len(s) - 1 - xs[j]))
        x_masks.append((number_or, number_and))
    return Mask(one_mask, tuple(x_masks))


def compute(s: str) -> int:
    memory = collections.defaultdict(int)

    mask = Mask(-1, ())
    lines = s.splitlines()
    for line in lines:
        if line.startswith('mask'):
            _, _, mask_s = line.partition(' = ')
            mask = parse_mask(mask_s)
        else:
            match = MEM_RE.match(line)
            assert match
            target = int(match[1])
            number = int(match[2])

            for target in mask.targets(target):
                memory[target] = number

    return sum(memory.values())


INPUT_S = '''\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 208),
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
