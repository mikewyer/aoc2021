"""Day 23"""

from __future__ import annotations
from collections import defaultdict, Counter
from dataclasses import dataclass
import os
import pytest
from typing import List, Optional, Tuple
from string import ascii_uppercase

INPUT = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

STATE1 = """.....A...
...B...E.
.F..C.D..
.....G..H
..I.N.JK.
L..M.O...
P.Q.R.ST.
.........
..U..V...
"""
# Which neighbour indexes to check
@dataclass
class Direction:
    name: str
    check: Tuple[int, int, int]


NORTH = Direction("N", (0, 1, 2))
SOUTH = Direction("S", (4, 5, 6))
EAST = Direction("E", (2, 3, 4))
WEST = Direction("W", (0, 6, 7))

DIRS = [NORTH, SOUTH, WEST, EAST]


class Grid:
    def __init__(self, start: List[str]) -> None:
        self.grid = defaultdict(Counter)
        self.elves: List[Elf] = []
        for i, row in enumerate(start):
            for j, char in enumerate(row):
                if char == "#":
                    self.grid[i][j] = -1
                    if len(self.elves) < 26:
                        name = ascii_uppercase[len(self.elves)]
                    else:
                        name = "#"
                    self.elves.append(Elf(i, j, name, self))

    def clear(self):
        for row in self.grid.values():
            empty = [i for i, j in row.items() if j > 0]
            for i in empty:
                row[i] = 0

    def run(self, count: int):
        for i in range(count):
            dir = i % 4
            # print(f"Round {i} Grid direction: {dir} : {DIRS[dir].name}")
            for e in self.elves:
                # print(f"Elf {e.name}")
                e.propose(dir)
            for e in self.elves:
                # print(f"Elf {e.name}")
                e.move()
            self.clear()

    def run_to_stop(self):
        moves = 1
        count = 0
        while moves:
            dir = count % 4
            # print(f"Round {i} Grid direction: {dir} : {DIRS[dir].name}")
            for e in self.elves:
                # print(f"Elf {e.name}")
                e.propose(dir)
            moves = 0
            for e in self.elves:
                # print(f"Elf {e.name}")
                moves += e.move()
            self.clear()
            count += 1
        return count

    def bounds(self):
        first_row = None
        last_row = None
        first_col = None
        last_col = None
        for i, row in sorted(self.grid.items()):
            for j, val in sorted(row.items()):
                if val == -1:
                    if first_row is None:
                        first_row = i
                    if last_row is None or i > last_row:
                        last_row = i
                    if first_col is None or j < first_col:
                        first_col = j
                    if last_col is None or j > last_col:
                        last_col = j
        return first_row, last_row, first_col, last_col

    def __str__(self) -> str:
        i_min, i_max, j_min, j_max = self.bounds()
        out = []
        for i in range(i_min, i_max + 1):
            row = []
            for j in range(j_min, j_max + 1):
                if self.grid[i][j] == -1:
                    row.append("#")
                else:
                    row.append(".")
            out.append("".join(row))
        return "\n".join(out) + "\n"

    def pretty(self) -> str:
        i_min, i_max, j_min, j_max = self.bounds()
        out = []
        for i in range(i_min, i_max + 1):
            row = []
            for j in range(j_min, j_max + 1):
                if self.grid[i][j] == -1:
                    for e in self.elves:
                        if e.i == i and e.j == j:
                            row.append(e.name)
                            break
                else:
                    row.append(".")
            out.append("".join(row))
        return "\n".join(out) + "\n"


@dataclass
class Elf:
    i: int  # row
    j: int  # col
    name: str
    grid: Grid
    prop_i: Optional[int] = None
    prop_j: Optional[int] = None

    def neighbours(self):
        i = self.i
        j = self.j
        g = self.grid.grid
        yield g[i - 1][j - 1]
        yield g[i - 1][j]
        yield g[i - 1][j + 1]
        yield g[i][j + 1]
        yield g[i + 1][j + 1]
        yield g[i + 1][j]
        yield g[i + 1][j - 1]
        yield g[i][j - 1]

    def propose(self, first_dir: int):
        ns = list(self.neighbours())
        self.prop_i = None
        self.prop_j = None
        if not any(i for i in ns if i < 0):
            return
        for each_dir in range(4):
            dir = DIRS[(first_dir + each_dir) % 4]
            if any(ns[i] for i in dir.check if ns[i] < 0):
                # print(f"{self.name} can't move {dir.name}")
                continue
            if dir is NORTH:
                self.prop_i = self.i - 1
                self.prop_j = self.j
            elif dir is SOUTH:
                self.prop_i = self.i + 1
                self.prop_j = self.j
            elif dir is EAST:
                self.prop_i = self.i
                self.prop_j = self.j + 1
            else:  # dir is WEST
                self.prop_i = self.i
                self.prop_j = self.j - 1
            self.grid.grid[self.prop_i][self.prop_j] += 1
            # print(
            #     f"{self.name} can move {dir.name} {self.i},{self.j} -> {self.prop_i}, {self.prop_j} ({self.grid.grid[self.prop_i][self.prop_j]})"
            # )

            break

    def move(self):
        if self.prop_i is None:
            return 0
        if self.grid.grid[self.prop_i][self.prop_j] == 1:
            # print(f"Move {self.i},{self.j} -> {self.prop_i}, {self.prop_j}")
            del self.grid.grid[self.i][self.j]
            self.i = self.prop_i
            self.j = self.prop_j
            self.grid.grid[self.i][self.j] = -1
            return 1
        return 0


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def test_example(example):
    grid = Grid(example)
    # print(grid)
    grid.run(1)
    # print(grid)
    assert grid.pretty() == STATE1


def test_example10(example):
    grid = Grid(example)
    grid.run(10)
    assert str(grid).count(".") == 110


def test_example_stop(example):
    grid = Grid(example)
    assert grid.run_to_stop() == 20


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    grid = Grid(inputs)
    grid.run(10)
    return str(grid).count(".")


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 4045


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Grid(inputs).run_to_stop()


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 963


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
