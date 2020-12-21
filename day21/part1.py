import argparse
import os.path
from typing import Dict
from typing import FrozenSet
from typing import NamedTuple
from typing import Set

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Recipe(NamedTuple):
    ingredients: FrozenSet[str]
    allergens: FrozenSet[str]


def compute(s: str) -> int:
    recipes = []
    for line in s.strip().splitlines():
        begin, _, rest = line.partition('(contains ')

        begin = begin.strip()
        ingredients = frozenset(begin.split())

        rest = rest.strip(')')
        allergens = frozenset(rest.split(', '))
        recipes.append(Recipe(ingredients, allergens))

    by_allergen: Dict[str, Set[str]] = {}
    for recipe in recipes:
        for allergen in recipe.allergens:
            by_allergen.setdefault(allergen, set(recipe.ingredients))
            by_allergen[allergen] &= recipe.ingredients

    assigned = {}
    while by_allergen:
        for k, v in tuple(by_allergen.items()):
            if len(v) == 1:
                val, = v
                assigned[k] = val
                for v in by_allergen.values():
                    v.discard(val)
                del by_allergen[k]

    all_ingredients: Set[str] = set()
    for recipe in recipes:
        all_ingredients |= recipe.ingredients

    total = 0
    known = set(assigned.values())
    for recipe in recipes:
        total += len(recipe.ingredients - known)
    return total


INPUT_S = '''\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
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
