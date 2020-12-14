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
    xs: Tuple[int, ...]

    def targets(self, number: int) -> Generator[int, None, None]:
        number = number | self.ones_mask
        number_s = list(f'{number:b}'.zfill(36))
        for i in range(1 << len(self.xs)):
            for j in range(len(self.xs)):
                number_s[self.xs[j]] = str((i & (1 << j)) >> j)
                yield int(''.join(number_s), 2)


def parse_mask(s: str) -> Mask:
    one_mask = int(s.replace('X', '0'), 2)
    x_pos = [match.start() for match in re.finditer('X', s)]
    return Mask(one_mask, tuple(x_pos))


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
