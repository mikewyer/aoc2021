"""Day X"""

from __future__ import annotations
import os
import pytest
import re
from typing import List

INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


class OutOfBounds(RuntimeError):
    """Sand outside known coords."""


class Cavern:
    def add_block(self, row: int, col: int):
        while len(self.rows) <= row:
            self.rows.append(set())
        self.rows[row].add(col)
        if not self.min_col or col < self.min_col:
            self.min_col = col
        if not self.max_col or col > self.max_col:
            self.max_col = col

    def __init__(self, blocks: List[str]) -> None:
        self.rows = [set()]
        self.min_col = None
        self.max_col = None
        self.has_floor = False
        for block in blocks:
            points = []
            for i in re.split(r" \-\> ", block):
                points.append([int(j) for j in i.split(",", 2)])
            start = points[0]
            for end in points[1:]:
                # print(f"{start} - {end}")
                for col in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                    for row in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                        self.add_block(row, col)
                start = end
            # print(self)

    def __str__(self) -> str:
        out = []
        for row_num, row in enumerate(self.rows):
            rowstr = [str(row_num), " "]
            for i in range(self.min_col, self.max_col + 1):
                rowstr.append("#" if i in row else " ")
            out.append("".join(rowstr))
        return "\n".join(out)

    def next_sand_pos(self, row: int, col: int) -> tuple:
        """Adds one piece of sand from the given point"""
        while row < len(self.rows) and col not in self.rows[row]:
            row += 1
        if row >= len(self.rows):
            return row, col
        if col - 1 not in self.rows[row]:
            if col == self.min_col and not self.has_floor:
                return row, col - 1
            return self.next_sand_pos(row, col - 1)
        if col + 1 not in self.rows[row]:
            if col == self.max_col and not self.has_floor:
                return row, col + 1
            return self.next_sand_pos(row, col + 1)
        return row - 1, col

    def add_sand(self) -> tuple:
        row, col = self.next_sand_pos(0, 500)
        if self.min_col <= col <= self.max_col and row < len(self.rows):
            self.add_block(row, col)
        elif self.has_floor:
            self.add_block(row, col)
        else:
            raise OutOfBounds(row, col, str(self))
        return row, col


class Floor:
    def __contains__(self, _: int) -> bool:
        return True


def test_example(example):
    cav = Cavern(example)
    print(cav)
    for i in range(24):
        cav.add_sand()
        print(i, cav)
    with pytest.raises(OutOfBounds):
        cav.add_sand()
    assert i == 23
    cav = Cavern(example)
    cav.rows.append(set())
    cav.rows.append(Floor())
    cav.has_floor = True
    row = 0
    col = 0
    i = 0
    while row != 0 or col != 500:
        row, col = cav.add_sand()
        i += 1
    assert i == 93


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    cav = Cavern(inputs)
    count = 0
    try:
        while 1:
            cav.add_sand()
            count += 1
    except OutOfBounds:
        return count


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 774


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    cav = Cavern(inputs)
    cav.rows.append(set())
    cav.rows.append(Floor())
    cav.has_floor = True
    row, col = 0, 0
    count = 0
    while row != 0 or col != 500:
        row, col = cav.add_sand()
        count += 1
    return count


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 22499


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
