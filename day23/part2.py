from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Node:
    def __init__(self, n: int) -> None:
        self.n = n
        self.next_node = self

    def __repr__(self) -> str:
        numbers = [self.n]
        next_node = self.next_node
        while next_node is not self:
            numbers.append(next_node.n)
            next_node = next_node.next_node
        return f'{type(self).__name__}({numbers!r})'

    def append(self, n: int) -> Node:
        new_node = type(self)(n)
        new_node.next_node = self.next_node
        self.next_node = new_node
        return self.next_node

    def pop3(self) -> Node:
        ret = self.next_node
        self.next_node = self.next_node.next_node.next_node.next_node
        return ret

    def push3(self, node3: Node) -> None:
        node3.next_node.next_node.next_node = self.next_node
        self.next_node = node3


def compute(s: str) -> int:
    numbers = [int(n) for n in list(s.strip())]

    nodes = {}
    nodes[numbers[0]] = current = Node(numbers[0])
    appender = current
    for number in numbers[1:]:
        nodes[number] = appender = appender.append(number)

    N = 1_000_000

    for i in range(len(numbers) + 1, N + 1):
        nodes[i] = appender = appender.append(i)

    for i in range(N * 10):
        taken = current.pop3()
        taken_n = {taken.n, taken.next_node.n, taken.next_node.next_node.n}

        current_label = (current.n - 1)
        if current_label == 0:
            current_label = N
        while current_label in taken_n:
            current_label = (current_label - 1)
            if current_label == 0:
                current_label = N

        nodes[current_label].push3(taken)

        current = current.next_node

    return nodes[1].next_node.n * nodes[1].next_node.next_node.n


INPUT_S = '''\
389125467
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 149245887792),
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
