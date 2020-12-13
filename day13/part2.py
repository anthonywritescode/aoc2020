import argparse
import os.path
from typing import Callable

import pytest
from sympy.ntheory.modular import crt
from z3 import Int
from z3 import sat
from z3 import Solver

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    parsed = [
        (int(s), i)
        for i, s in enumerate(lines[1].split(','))
        if s != 'x'
    ]
    buses = [pt[0] for pt in parsed]
    mods = [-1 * pt[1] for pt in parsed]

    return crt(buses, mods)[0]


def compute_z3(s: str) -> int:
    lines = s.splitlines()
    parsed = [
        (int(s), i)
        for i, s in enumerate(lines[1].split(','))
        if s != 'x'
    ]

    T = Int('T')
    N = Int('N')

    t = 0
    mult = parsed[0][0]

    for bus, offset in parsed[1:]:
        solver = Solver()
        solver.add(T > 0, (T + offset) % bus == 0)
        solver.add(T == t + N * mult)
        assert solver.check() == sat
        t = solver.model()[T]
        mult *= bus

    return t


def compute_loop(s: str) -> int:
    lines = s.splitlines()
    parsed = [
        (int(s), i)
        for i, s in enumerate(lines[1].split(','))
        if s != 'x'
    ]

    t = 0
    mult = parsed[0][0]

    for bus, offset in parsed[1:]:
        while (t + offset) % bus != 0:
            t += mult
        mult *= bus

    return t


INPUT_S = '''\
939
7,13,x,x,59,x,31,19
'''
INPUT2_S = '''\
...
17,x,13,19
'''
INPUT3_S = '''\
...
67,7,59,61
'''
INPUT4_S = '''\
...
67,x,7,59,61
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1068781),
        (INPUT2_S, 3417),
        (INPUT3_S, 754018),
        (INPUT4_S, 779210),
        ('...\n5,7', 20),
        ('...\n5,7,9', 160),
    ),
)
@pytest.mark.parametrize('func', (compute, compute_z3, compute_loop))
def test(input_s: str, expected: int, func: Callable[[str], int]) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        contents = f.read()
    with timing('sympy'):
        print(compute(contents))
    with timing('z3'):
        print(compute_z3(contents))
    with timing('loop'):
        print(compute_loop(contents))

    return 0


if __name__ == '__main__':
    exit(main())
