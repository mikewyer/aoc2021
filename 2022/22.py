"""Day 22"""

from __future__ import annotations
from dataclasses import dataclass
import os
import pytest
import re
from typing import List

INPUT = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


@pytest.fixture
def example() -> List[str]:
    return [i.strip("\n") for i in INPUT.splitlines()]


dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
RIGHT, DOWN, LEFT, UP = 0, 1, 2, 3


def remap(row: int, col: int, dir: int):
    #         1
    #       5 0
    #     0 0 0
    #   0   a b
    #  50   c
    # 100 d e
    # 150 f

    # Moving up (dir == 3)
    if dir == UP:
        if row == -1:
            if 50 <= col < 100:
                # a -> f
                return 150 + (col - 50), 0, RIGHT
            else:
                # b -> f
                assert col >= 100
                return 199, col - 100, UP
        if row == 99 and col < 50:
            # d -> c
            return 50 + col, 50, RIGHT
    if dir == DOWN:
        if row == 50 and col >= 100:
            # b -> c
            return 50 + (col - 100), 99, LEFT
        if row == 150 and 50 <= col < 100:
            # e -> f
            return 150 + (col - 50), 49, LEFT
        if row == 200:
            # f -> b
            assert col < 50
            return 0, col + 100, DOWN
    if dir == LEFT:
        if col == -1:
            if 100 <= row < 150:
                # d -> a
                return (49 - (row - 100)), 50, RIGHT
            else:
                # f -> a
                assert row >= 150
                return 0, row - 100, DOWN
        if col == 49 and row < 100:
            if row < 50:
                # a -> d
                return 100 + (49 - row), 0, RIGHT
            else:
                # c -> d
                return 100, row - 50, DOWN
    if dir == RIGHT:
        if col == 150:
            # b -> e
            assert row < 50
            return 100 + (49 - row), 99, LEFT
        if col == 100 and 50 <= row:
            if row < 100:
                # c -> b
                return 49, row + 50, UP
            else:
                assert row < 150
                # e -> b
                return 149 - row, 149, LEFT
        if col == 50 and 150 <= row:
            # f -> e
            assert row < 200
            return 149, row - 100, UP
    return row, col, dir


@dataclass
class Board:
    rows: list
    moves: str = ""

    def __post_init__(self):
        self.moves = self.rows.pop()
        self.rows.pop()

    def first(self) -> tuple:
        return (0, self.rows[0].find("."))

    def next(self, row: int, col: int, dir: int):
        new_row = row
        new_col = col
        d_row, d_col = dirs[dir]
        print(f"{row}({d_row}) {col}({d_col}) {dir}")
        if d_row:
            seen = set()
            new_row = (row + d_row) % len(self.rows)
            while col >= len(self.rows[new_row]) or self.rows[new_row][col] == " ":
                new_row = (new_row + d_row) % len(self.rows)
                assert new_row not in seen
                seen.add(new_row)
        if d_col:
            seen = set()
            new_col = (col + d_col) % len(self.rows[row])
            while self.rows[row][new_col] == " ":
                new_col = (new_col + d_col) % len(self.rows[row])
                assert new_col not in seen
                seen.add(new_col)
        return new_row, new_col, self.rows[new_row][new_col]

    def remap(self, row: int, col: int, dir: int):
        new_row, new_col, new_dir = remap(row, col, dir)
        assert 0 <= new_row < len(self.rows)
        assert 0 <= new_col < len(self.rows[new_row])
        assert self.rows[new_row][new_col] in [".", "#"]
        # print(f"  Remap {row},{col} {dir} => {new_row},{new_col} {new_dir}")
        return new_row, new_col, new_dir

    def next_cube(self, row: int, col: int, dir: int):
        d_row, d_col = dirs[dir]
        return self.remap(row + d_row, col + d_col, dir)

    def move(self, start_row: int, start_col: int, dir: int, count: int):
        new_row = start_row
        new_col = start_col
        for _ in range(count):
            next_row, next_col, value = self.next(new_row, new_col, dir)
            if value == "#":
                # print("#")
                return new_row, new_col
            new_row, new_col = next_row, next_col
        return new_row, new_col

    def move_cube(
        self,
        start_row: int,
        start_col: int,
        dir: int,
        count: int,
        stop_at_wall: bool = True,
        verbose: bool = False,
    ):
        new_row = start_row
        new_col = start_col
        new_dir = dir
        for i in range(count):
            next_row, next_col, next_dir = self.next_cube(new_row, new_col, new_dir)
            if self.rows[next_row][next_col] == "#" and stop_at_wall:
                # print("#")
                break
            new_row, new_col, new_dir = next_row, next_col, next_dir
            if verbose:
                print(f"  {i} .. {new_row},{new_col} {new_dir}")
        return new_row, new_col, new_dir

    def path(self) -> int:
        dir = 0
        row, col = self.first()
        for instr in re.split(r"([RL])", self.moves):
            if instr == "R":
                dir = (dir + 1) % 4
            elif instr == "L":
                dir = (dir - 1) % 4
            else:
                print(f"{row},{col} {int(instr)} {dir}")
                row, col = self.move(row, col, dir, int(instr))
        return (row + 1) * 1000 + (col + 1) * 4 + dir

    def path_cube(self) -> int:
        dir = 0
        row, col = self.first()
        for instr in re.split(r"([RL])", self.moves):
            if instr == "R":
                dir = (dir + 1) % 4
                print(f"R => {dir}")
            elif instr == "L":
                dir = (dir - 1) % 4
                print(f"L => {dir}")
            else:
                print(f"MV {row},{col} {int(instr)} {dir}")
                row, col, dir = self.move_cube(row, col, dir, int(instr))
                print(f"AT {row},{col} {dir}")
        return (row + 1) * 1000 + (col + 1) * 4 + dir


def test_example(example):
    board = Board(example)
    assert board.path() == 6032


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Board(inputs)


def test_part1() -> None:
    inputs = get_inputs()
    board = part1(inputs)
    assert board.first() == (0, 50)
    result = board.path()
    assert result > 4320  # First attempt
    assert result == 56372


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    return Board(inputs)


def test_part2() -> None:
    inputs = get_inputs()
    board = part2(inputs)
    assert board.remap(-1, 50, UP) == (150, 0, RIGHT)
    assert board.remap(-1, 99, UP) == (199, 0, RIGHT)
    assert board.remap(-1, 100, UP) == (199, 0, UP)
    assert board.remap(-1, 149, UP) == (199, 49, UP)
    assert board.remap(99, 0, UP) == (50, 50, RIGHT)
    assert board.remap(99, 49, UP) == (99, 50, RIGHT)
    assert board.remap(99, 50, UP) == (99, 50, UP)
    assert board.remap(99, 99, UP) == (99, 99, UP)

    # Circuit from origin RIGHT
    x, y, new_dir = board.move_cube(0, 50, RIGHT, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (0, 100, RIGHT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (149, 99, LEFT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (149, 49, LEFT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (0, 50, RIGHT)

    # Circuit from origin LEFT
    x, y, new_dir = board.move_cube(0, 50, LEFT, 50, stop_at_wall=False, verbose=True)
    assert board.next_cube(0, 50, LEFT) == (149, 0, RIGHT)
    assert board.next_cube(149, 0, RIGHT) == (149, 1, RIGHT)
    assert board.next_cube(149, 1, RIGHT) == (149, 2, RIGHT)
    assert (x, y, new_dir) == (149, 49, RIGHT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (149, 99, RIGHT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (0, 100, LEFT)
    x, y, new_dir = board.move_cube(x, y, new_dir, 50, stop_at_wall=False)
    assert (x, y, new_dir) == (0, 50, LEFT)

    # for dir in [RIGHT, LEFT, UP, DOWN]:
    #     for i, row in enumerate(board.rows):
    #         for j, val in enumerate(row):
    #             if val in [".", "#"]:
    #                 x, y, new_dir = board.move_cube(i, j, dir, 200, stop_at_wall=False)
    #                 print(f"{i},{j} {dir} -> {x},{y} {new_dir}")
    #                 assert x == i
    #                 assert y == j
    #                 assert new_dir == dir

    # aL -> dR
    assert board.remap(0, 49, LEFT) == (149, 0, RIGHT)
    assert board.remap(49, 49, LEFT) == (100, 0, RIGHT)
    # cL -> dD
    assert board.remap(50, 49, LEFT) == (100, 0, DOWN)
    assert board.remap(99, 49, LEFT) == (100, 49, DOWN)
    # dL -> aR
    assert board.remap(100, -1, LEFT) == (49, 50, RIGHT)
    assert board.remap(149, -1, LEFT) == (0, 50, RIGHT)
    # fL -> aD
    assert board.remap(150, -1, LEFT) == (0, 50, DOWN)
    assert board.remap(199, -1, LEFT) == (0, 99, DOWN)

    # bR -> eL
    assert board.remap(0, 150, RIGHT) == (149, 99, LEFT)
    assert board.remap(49, 150, RIGHT) == (100, 99, LEFT)
    # cR -> bU
    assert board.remap(50, 100, RIGHT) == (49, 100, UP)
    assert board.remap(99, 100, RIGHT) == (49, 149, UP)
    # eR -> bL
    assert board.remap(100, 100, RIGHT) == (49, 149, LEFT)
    assert board.remap(149, 100, RIGHT) == (0, 149, LEFT)
    # fR -> eU
    assert board.remap(150, 50, RIGHT) == (149, 50, UP)
    assert board.remap(199, 50, RIGHT) == (149, 99, UP)

    # bD -> cL
    assert board.remap(50, 100, DOWN) == (50, 99, LEFT)
    assert board.remap(50, 149, DOWN) == (99, 99, LEFT)

    # eD -> fL
    assert board.remap(150, 50, DOWN) == (150, 49, LEFT)
    assert board.remap(150, 99, DOWN) == (199, 49, LEFT)

    # fD -> bD
    assert board.remap(200, 0, DOWN) == (0, 100, DOWN)
    assert board.remap(200, 49, DOWN) == (0, 149, DOWN)

    result = board.path_cube()
    assert result > 75401
    assert result == 197047


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".txt"):
        return [i.strip("\n") for i in open(base + ".txt")]
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
