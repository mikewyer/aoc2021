"""Day 14"""

import os
import pytest
import timeit
from typing import Dict, Iterable, List, Tuple
from functools import cache


@pytest.fixture
def example() -> List[str]:
    return """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()


def charpair(input: str) -> Iterable[str]:
    for i in range(0, len(input) - 1):
        yield input[i : i + 2]


def count_chars(chain: str):
    counts: Dict[str, int] = {}
    for char in chain:
        counts.setdefault(char, 0)
        counts[char] += 1
    return counts


class Polymer:
    def __init__(self, rules: List[str]) -> None:
        self.link_dict: Dict[str, str] = {}
        for rule in rules:
            key, new_char = rule.split(" -> ")
            self.link_dict[key] = key[0] + new_char

    def link(self, chain: str):
        output = []
        for chunk in charpair(chain):
            output.append(self.link_dict[chunk])
        output.append(chain[-1])
        return "".join(output)

    @cache
    def count_rec(
        self, chain: str, links: int, limit: int = 5, char_limit=512
    ) -> Dict[str, int]:
        if links < 0:
            raise RuntimeError("-ve links")
        if links == 0:
            return count_chars(chain)
        if links < limit:
            new_chain = self.link(chain)
            for _ in range(links - 1):
                new_chain = self.link(new_chain)
            return count_chars(new_chain)
        if len(chain) <= char_limit:
            new_chain = self.link(chain)
            return self.count_rec(new_chain, links - 1, limit, char_limit)
        totals: Dict[str, int] = {}
        for sub_chain in charpair(chain):
            for char, count in self.count_rec(
                sub_chain, links, limit, char_limit
            ).items():
                totals.setdefault(char, 0)
                totals[char] += count
            totals[sub_chain[-1]] -= 1
        totals.setdefault(chain[-1], 0)
        totals[chain[-1]] += 1
        return totals


def min_max(counts: Dict[str, int]) -> Tuple[int, int]:
    min_i = -1
    max_i = 0
    for i in counts.values():
        if min_i < 0 or i < min_i:
            min_i = i
        if i > max_i:
            max_i = i
    return min_i, max_i


def test_example(example: List[str]):
    chain: str = example[0]
    polymer = Polymer(example[2:])
    chain = polymer.link(chain)
    assert chain == "NCNBCHB"
    assert polymer.link(chain) == "NBCCNBBBCBHCB"
    for _ in range(9):
        chain = polymer.link(chain)
    assert len(chain) == 3073
    counts = count_chars(chain)
    assert counts["B"] == 1749
    assert counts["C"] == 298
    assert counts["H"] == 161
    assert counts["N"] == 865
    min_count, max_count = min_max(counts)
    assert max_count - min_count == 1588


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    chain = inputs[0]
    polymer = Polymer(inputs[2:])
    for _ in range(10):
        chain = polymer.link(chain)
    counts = count_chars(chain)
    min_count, max_count = min_max(counts)
    return max_count - min_count


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 2621


def test_example2(example: List[str]):
    chain: str = example[0]
    polymer = Polymer(example[2:])
    counts = polymer.count_rec(chain, 10)
    assert sum(counts.values()) == 3073
    assert counts["B"] == 1749
    assert counts["C"] == 298
    assert counts["H"] == 161
    assert counts["N"] == 865

    counts = polymer.count_rec(chain, 40)
    assert counts["B"] == 2192039569602
    assert counts["H"] == 3849876073


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    chain = inputs[0]
    polymer = Polymer(inputs[2:])
    # for link_limit in range(2, 10):
    #     for char_limit in range(3, 20):
    #         times = timeit.timeit(
    #             lambda: polymer.count_rec(
    #                 chain, 40, limit=link_limit, char_limit=char_limit
    #             ),
    #             number=10,
    #         )
    #         print(f"{link_limit} {char_limit} {times}")
    counts = polymer.count_rec(chain, 40, limit=3, char_limit=3)
    min_count, max_count = min_max(counts)
    return max_count - min_count


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2843834241366


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def test_get_inputs() -> None:
    inputs = get_inputs()
    assert len(inputs) > 0


if __name__ == "__main__":
    test_get_inputs()
    inputs = get_inputs()
    print(part1(inputs))
    test_part1()
    print(part2(inputs))
    test_part2()
