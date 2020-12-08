import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    code = []
    for line in s.splitlines():
        opc, n_s = line.split()
        n = int(n_s)
        code.append((opc, n))

    visited = set()
    n = 0
    pc = 0
    while pc not in visited:
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

    return n


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
        (INPUT_S, 5),
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
