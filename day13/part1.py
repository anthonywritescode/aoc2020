import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    start_time = int(lines[0])

    busses = [int(s) for s in lines[1].split(',') if s != 'x']

    minimum = busses[0] * (start_time // busses[0] + 1)
    bus_id = busses[0]
    for bus in busses[1:]:
        n = start_time // bus
        depart_time = bus * (n + 1)
        if depart_time < minimum:
            minimum = depart_time
            bus_id = bus
    return bus_id * (minimum - start_time)


INPUT_S = '''\
939
7,13,x,x,59,x,31,19
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 295),
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
