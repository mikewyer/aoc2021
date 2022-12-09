"""Day 9"""

from __future__ import annotations
from dataclasses import dataclass
import os
import pytest
from typing import List

INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

vector = {
    "R": lambda x, y, n: (x + n, y),
    "L": lambda x, y, n: (x - n, y),
    "U": lambda x, y, n: (x, y + n),
    "D": lambda x, y, n: (x, y - n),
}


@dataclass
class End:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    def move_head(self, dir: str):
        self.x, self.y = vector[dir](self.x, self.y, 1)

    def move_tail(self, head: End):
        diff_x = head.x - self.x
        diff_y = head.y - self.y
        mv_x = 0
        mv_y = 0
        if abs(diff_x) == 2:
            mv_x = 1 if diff_x == 2 else -1
            if diff_y:
                mv_y = 1 if diff_y > 0 else -1
        elif abs(diff_y) == 2:
            mv_y = 1 if diff_y == 2 else -1
            if diff_x:
                mv_x = 1 if diff_x > 0 else -1
        self.x = self.x + mv_x
        self.y = self.y + mv_y


class Grid:
    def __init__(self, ropes: int = 2) -> None:
        self.ropes = [End(0, 0) for _ in range(ropes)]
        self.seen = [set(["0,0"]) for _ in range(ropes)]

    def move(self, dir: str, count: int):
        for i in range(count):
            for i, rope in enumerate(self.ropes):
                if i == 0:
                    rope.move_head(dir)
                else:
                    rope.move_tail(self.ropes[i - 1])
                self.seen[i].add(str(self.ropes[i]))


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


@pytest.fixture
def example2() -> List[str]:
    return [
        i.strip()
        for i in """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()
    ]


def test_example(example):
    grid = Grid()
    grid10 = Grid(10)
    for row in example:
        dir, count = row.split(" ")
        grid.move(dir, int(count))
        grid10.move(dir, int(count))
    print(grid.seen[1])
    assert len(grid.seen[1]) == 13
    assert len(grid10.seen[9]) == 1


def test_example2(example2):
    grid10 = Grid(10)
    for row in example2:
        dir, count = row.split(" ")
        grid10.move(dir, int(count))
    # print(grid.seen)
    assert len(grid10.seen[9]) == 36


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    grid = Grid()
    for row in inputs:
        dir, count = row.split(" ")
        grid.move(dir, int(count))
    # print(grid.seen)
    return len(grid.seen[1])


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 6087


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    grid = Grid(10)
    for row in inputs:
        dir, count = row.split(" ")
        grid.move(dir, int(count))
    # print(grid.seen)
    return len(grid.seen[9])


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2493


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
