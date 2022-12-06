"""Day X"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> str:
    input = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
    return input


def unique_index(input: str, length: int = 4) -> int:
    for i in range(length, len(input)):
        chunk = input[i - length : i]
        if len(set(list(chunk))) == length:
            return i


def test_example(example):
    assert unique_index(example) == 7
    assert unique_index("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert unique_index("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert unique_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return unique_index(inputs[0])


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1909


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return unique_index(inputs[0], 14)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 3380


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
