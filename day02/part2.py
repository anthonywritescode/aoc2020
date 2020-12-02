import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    counter = 0
    for line in s.splitlines():
        r, c, p = line.split()
        r_start_s, r_end_s = r.split('-')
        r_start, r_end = int(r_start_s), int(r_end_s)
        c = c[0]

        if (p[r_start - 1] == c) ^ (p[r_end - 1] == c):
            counter += 1

    return counter


INPUT_S = '''\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
