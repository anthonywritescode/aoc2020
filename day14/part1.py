import argparse
import collections
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MEM_RE = re.compile(r'^mem\[(\d+)\] = (\d+)$')


def compute(s: str) -> int:
    memory = collections.defaultdict(int)

    mask_or = 0
    mask_and = -1
    lines = s.splitlines()
    for line in lines:
        if line.startswith('mask'):
            _, _, mask_s = line.partition(' = ')
            mask_or = int(mask_s.replace('X', '0'), 2)
            mask_and = int(mask_s.replace('X', '1'), 2)
        else:
            match = MEM_RE.match(line)
            assert match
            target = int(match[1])
            number = int(match[2])
            masked = (number | mask_or) & mask_and
            memory[target] = masked

    return sum(memory.values())


INPUT_S = '''\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 165),
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
