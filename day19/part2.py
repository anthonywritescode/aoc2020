import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    rules, lines = s.split('\n\n')

    rules_s = {}
    for line in rules.splitlines():
        k, _, v = line.partition(': ')
        rules_s[k] = v

    def _get_re(s: str) -> str:
        if s == '|':
            return s

        rule_s = rules_s[s]
        if rule_s.startswith('"'):
            return rule_s.strip('"')
        else:
            return f'({"".join(_get_re(part) for part in rule_s.split())})'

    re_42 = re.compile(_get_re('42'))
    re_31 = re.compile(_get_re('31'))

    count = 0
    for line in lines.splitlines():
        pos = 0

        count_42 = 0
        while match := re_42.match(line, pos):
            count_42 += 1
            pos = match.end()

        count_31 = 0
        while match := re_31.match(line, pos):
            count_31 += 1
            pos = match.end()

        if 0 < count_31 < count_42 and pos == len(line):
            count += 1

    return count


INPUT_S = '''\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''

INPUT_2_S = INPUT_S.split('\n\n')[0] + '\n\naaaabbaaaabbaaa'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 12),
        (INPUT_2_S, 0),
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
