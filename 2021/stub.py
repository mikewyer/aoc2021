"""Day X"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> List[str]:
    return """
    """.splitlines()


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return 0


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1


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
