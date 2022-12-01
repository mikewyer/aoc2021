"""Day X"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> List[str]:
    return """forward 5
down 5
forward 8
up 3
down 8
forward 2""".splitlines()


def go_sub(inputs: List[str]):
    pos = 0
    depth = 0

    def down(x):
        nonlocal depth
        depth += x

    def up(x):
        nonlocal depth
        depth -= x

    def forward(x):
        nonlocal pos
        pos += x

    move = {"down": down, "up": up, "forward": forward}
    for command in inputs:
        cmd, num = command.split(" ")
        move[cmd](int(num))
    return pos, depth


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    x, y = go_sub(inputs)
    return x * y


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1813801


def go_sub2(inputs: List[str]):
    pos = 0
    depth = 0
    aim = 0

    def down(x):
        nonlocal aim
        aim += x

    def up(x):
        nonlocal aim
        aim -= x

    def forward(x):
        nonlocal pos, aim, depth
        pos += x
        depth += aim * x

    move = {"down": down, "up": up, "forward": forward}
    for command in inputs:
        cmd, num = command.split(" ")
        move[cmd](int(num))
    return pos, depth


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    x, y = go_sub2(inputs)
    return x * y


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1960569556


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
