"""Day 13"""

from functools import cmp_to_key
from itertools import zip_longest
import os
import pytest
import re
from typing import Iterator, List, Tuple

INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
# [[8,[[7,10,10,5],[8,4,9]],3,5],[[[3,9,4],5,[7,5,5]],[[3,2,5],[10],[5,5],0,[8]]],[4,2,[],[[7,5,6,3,0],[4,4,10,7],6,[8,10,9]]],[[4,[],4],10,1]]
# [[[[8],[3,10],[7,6,3,7,4],1,8]]]

# [[8,[[7]]]]
# [[[[8]]]]
# """


class ParseError(Exception):
    """Found an unexpected situation when parsing."""


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def by_pair(input: List[str]) -> Iterator[Tuple[str, str]]:
    rows: List[str] = []
    for row in input:
        if row.strip() == "":
            yield rows[0], rows[1]
            rows = []
        else:
            rows.append(row)
    if rows:
        yield rows[0], rows[1]


def validate(left, right):
    for (
        l,
        r,
    ) in zip_longest(left, right):
        if r is None:
            return 1
        if l is None:
            return -1
        if isinstance(l, list):
            if isinstance(r, list):
                if result := validate(l, r):
                    return result
                continue
            if isinstance(r, int):
                if result := validate(l, [r]):
                    return result
                continue
            assert False
        if isinstance(r, list):
            if isinstance(l, int):
                if result := validate([l], r):
                    return result
                continue
            assert False
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return -1
            elif l > r:
                return 1
            continue
        assert False
    return 0


def test_example(example):
    parsed = []
    failed = 0
    for i, (left, right) in enumerate(by_pair(example)):
        cmp = validate(eval(left), eval(right))
        if cmp == -1:
            parsed.append(i + 1)
        else:
            failed += 1
    assert parsed == [1, 2, 4, 6]
    assert failed == 4
    assert sum(parsed) == 13


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    parsed = []
    for i, (left, right) in enumerate(by_pair(inputs)):
        cmp = validate(eval(left), eval(right))
        if cmp == -1:
            parsed.append(i + 1)
    return sum(parsed)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 6420


def find_markers(inputs: List[str]) -> int:
    packets = [eval(i) for i in inputs if i]
    marker1 = [[2]]
    marker2 = [[6]]
    packets.append(marker1)
    packets.append(marker2)
    packets.sort(key=cmp_to_key(validate))
    ind1 = packets.index(marker1)
    ind2 = packets.index(marker2)
    return (ind1 + 1) * (ind2 + 1)


def test_example2(example):
    assert find_markers(example) == 140


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return find_markers(inputs)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 22000


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
