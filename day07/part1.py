import argparse
import collections
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PATTERN = re.compile(
    r'^([^ ]+ [^ ]+) bags contain '
    r'(no other bags|((, )?(\d+) ([^ ]+ [^ ]+) bags?)*)\.$'
)
BAG_RE = re.compile(r'(\d+) ([^ ]+ [^ ]+)')


def compute(s: str) -> int:
    parents = collections.defaultdict(list)
    for line in s.splitlines():
        match = PATTERN.match(line)
        assert match
        k = match[1]
        targets = [(int(n), tp) for n, tp in BAG_RE.findall(match[2])]
        for _, color in targets:
            parents[color].append(k)

    total_colors = set()
    parents_queue = parents['shiny gold']
    while parents_queue:
        color = parents_queue.pop()
        if color not in total_colors:
            total_colors.add(color)
            parents_queue.extend(parents[color])

    return len(total_colors)


INPUT_S = '''\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 4),
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
