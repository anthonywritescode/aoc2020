import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    numbers = set()
    for n_s in s.split():
        n = int(n_s)
        numbers.add(n)
        if 2020 - n in numbers:
            return (2020 - n) * n
    else:
        raise NotImplementedError


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1721 979 366 299 675 1456', 514579),
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
