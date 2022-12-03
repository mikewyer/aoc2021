"""Day X"""

import os
import pytest
from typing import List
from functools import lru_cache
import string


@pytest.fixture
def example() -> List[str]:
    return [
        i.strip()
        for i in """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()
    ]


def common_char(a: str, b: str, c: str = "") -> str:
    seen = set()
    for char in a:
        if char in seen:
            continue
        seen.add(char)
        if char in b:
            if not c or char in c:
                return char


def comparts(bags: List[str]):
    for bag in bags:
        assert len(bag) % 2 == 0
        count = len(bag) // 2
        yield (bag[0:count], bag[count:])


def split_by(batch: int, rows: List[str]):
    group = []
    for item in rows:
        group.append(item)
        if len(group) == batch:
            yield group
            group = []
    if group:
        yield (group)


@lru_cache(maxsize=52)
def score(char: str) -> int:
    return string.ascii_letters.find(char) + 1


def test_example(example):
    bags = list(comparts(example))
    assert bags[0] == ("vJrwpWtwJgWr", "hcsFMMfFFhFp")
    assert common_char(*bags[0]) == "p"
    assert score("p") == 16
    assert sum(score(common_char(*i)) for i in bags) == 157
    groups = list(split_by(3, example))
    assert common_char(*groups[0]) == "r"
    assert common_char(*groups[1]) == "Z"
    assert sum(score(common_char(*i)) for i in groups) == 70


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return sum(score(common_char(*i)) for i in comparts(inputs))


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 8053


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return sum(score(common_char(*i)) for i in split_by(3, inputs))


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2425


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".txt"):
        return [i.strip() for i in open(base + ".txt")]
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
