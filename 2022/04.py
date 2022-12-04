"""Day X"""

import os
import pytest
from typing import List

INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def pairs(lines: List[str]):
    for row in lines:
        a, b = row.split(",")
        yield ([int(i) for i in a.split("-")], [int(i) for i in b.split("-")])


def count_overlaps(input: List[str]) -> int:
    count = 0
    for a, b in pairs(input):
        # sort
        if a[0] > b[0] or (a[0] == b[0] and a[1] <= b[1]):
            a, b = b, a
        if b[0] >= a[0] and b[1] <= a[1]:
            count += 1
    return count


def has_overlap(a0, a1, b0, b1) -> bool:
    if a0 in range(b0, b1 + 1):
        return True
    if a1 in range(b0, b1 + 1):
        return True
    if b0 in range(a0, a1 + 1):
        return True
    if b1 in range(a0, a1 + 1):
        return True
    return False


def count_any_overlaps(input: List[str]) -> int:
    count = 0
    for (
        a,
        b,
    ) in pairs(input):
        if has_overlap(a[0], a[1], b[0], b[1]):
            count += 1
    return count


def test_example(example):
    assert count_overlaps(example) == 2
    assert count_any_overlaps(example) == 4


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return count_overlaps(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 532


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return count_any_overlaps(inputs)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 854


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
