import argparse
import os.path
from typing import List
from typing import Tuple

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def run(code: List[Tuple[str, int]]) -> int:
    visited = set()
    n = 0
    pc = 0
    while pc not in visited and pc < len(code):
        visited.add(pc)
        opc, value = code[pc]
        if opc == 'acc':
            n += value
            pc += 1
        elif opc == 'jmp':
            pc += value
        elif opc == 'nop':
            pc += 1
        else:
            raise NotImplementedError(opc)

    if pc == len(code):
        return n
    else:
        raise RuntimeError('wat')


def compute(s: str) -> int:
    code = []
    for line in s.splitlines():
        opc, n_s = line.split()
        n = int(n_s)
        code.append((opc, n))

    for i, (opc, value) in enumerate(code):
        if opc == 'nop':
            code2 = code[:]
            code2[i] = ('jmp', value)
            try:
                return run(code2)
            except RuntimeError:
                pass
        elif opc == 'jmp':
            code2 = code[:]
            code2[i] = ('nop', value)
            try:
                return run(code2)
            except RuntimeError:
                pass

    raise NotImplementedError('wat')


INPUT_S = '''\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 8),
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
