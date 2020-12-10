import argparse
import functools
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@functools.lru_cache(maxsize=None)
def n_for_streak(n: int) -> int:
    assert n >= 2
    if n == 2:
        return 1
    elif n == 3:
        return 2
    elif n == 4:
        return 4
    else:
        return n_for_streak(n - 1) + n_for_streak(n - 2) + n_for_streak(n - 3)


def compute(s: str) -> int:
    numbers = sorted(int(line) for line in s.splitlines())
    numbers.insert(0, 0)

    combs = 1

    prev = numbers[0]
    streak = 1
    for n in numbers[1:]:
        if n == prev + 1:
            streak += 1
        elif streak > 1:
            combs *= n_for_streak(streak)
            streak = 1
        prev = n

    if streak > 1:
        combs *= n_for_streak(streak)

    return combs


INPUT_S = '''\
16
10
15
5
1
11
7
19
6
12
4
'''

INPUT_S2 = '''\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 8),
        (INPUT_S2, 19208),
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
