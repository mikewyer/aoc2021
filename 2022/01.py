"""Day X"""

import os
import pytest
from typing import List


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".txt"):
        return [i.strip() for i in open(base + ".txt")]
    return []


@pytest.fixture
def example() -> List[str]:
    return """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".splitlines()


def split_elves(lines: List[str]):
    elves: List[int] = []
    elf = 0
    for line in lines:
        if cals := line.strip():
            elf += int(cals)
        else:
            elves.append(elf)
            elf = 0
    if elf:
        elves.append(elf)
    return elves


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return max(split_elves(inputs))


def test_example(example):
    assert part1(example) == 24000


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 72602


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    top3 = sorted(split_elves(inputs), reverse=True)[0:3]
    return sum(top3)


def test_example2(example):
    assert part2(example) == 45000


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 207410


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
