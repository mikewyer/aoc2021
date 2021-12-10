"""Day 11"""

from __future__ import annotations
import os
import pytest
from typing import Dict, Iterable, List, Tuple


@pytest.fixture
def example() -> List[str]:
    return """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines()


class LifeGrid:
    def __init__(self, rows: Iterable[str]) -> None:
        self.rows = list(rows)
        self.max_y = len(self.rows)
        self.max_x = len(self.rows[0])

    @property
    def count(self):
        return sum([j.count("#") for j in self.rows])

    def neighbours(self, x, y):
        for other_y in range(max(0, y - 1), min(self.max_y, y + 2)):
            for other_x in range(max(0, x - 1), min(self.max_x, x + 2)):
                if other_x == x and other_y == y:
                    continue
                yield other_x, other_y

    def adjacent(self, x, y) -> Dict[str, int]:
        # print(f"{x},{y}:")
        cells: Dict[str, int] = {".": 0, "L": 0, "#": 0}
        for other_x, other_y in self.neighbours(x, y):
            cells[self.rows[other_y][other_x]] += 1
        return cells

    def lines(self, x, y) -> Dict[str, int]:
        cells: Dict[str, int] = {".": 0, "L": 0, "#": 0}
        for other_x, other_y in self.neighbours(x, y):
            x_delta = other_x - x
            y_delta = other_y - y
            while (
                other_x in range(0, self.max_x)
                and other_y in range(0, self.max_y)
                and self.rows[other_y][other_x] == "."
            ):
                other_x += x_delta
                other_y += y_delta
            if other_x in range(0, self.max_x) and other_y in range(0, self.max_y):
                cells[self.rows[other_y][other_x]] += 1
        return cells

    def process_row(self, y: int, use_lines: bool = False) -> Tuple[str, bool]:
        row = []
        changed = False
        count_cells = self.adjacent
        threshold = 4
        if use_lines:
            count_cells = self.lines
            threshold = 5
        for x, cell in enumerate(self.rows[y]):
            if cell == ".":
                row.append(".")
                continue
            adj_count = count_cells(x, y)
            if cell == "L" and adj_count["#"] == 0:
                row.append("#")
                changed = True
            elif cell == "#" and adj_count["#"] >= threshold:
                row.append("L")
                changed = True
            else:
                row.append(cell)
        return "".join(row), changed

    def round(self, use_lines=False) -> Tuple[LifeGrid, bool]:
        changed = False
        new_grid = []
        for y in range(0, self.max_y):
            new_row, row_change = self.process_row(y, use_lines=use_lines)
            if row_change:
                changed = True
            new_grid.append(new_row)
        return self.__class__(new_grid), changed


def test_grid(example: List[str]):
    grid = LifeGrid(example)
    assert grid.count == 0
    grid, changed = grid.round()
    assert grid.rows[0] == "#.##.##.##"
    assert changed
    for row in grid.rows:
        assert "L" not in row
    assert grid.adjacent(3, 0) == {"#": 4, "L": 0, ".": 1}
    grid, changed = grid.round()
    assert changed
    assert grid.rows[0] == "#.LL.L#.##"
    assert grid.count == 20
    for _ in range(4):
        grid, changed = grid.round()
    assert not changed
    assert grid.count == 37


def test_grid_lines(example: List[str]):
    grid = LifeGrid(example)
    for _ in range(8):
        grid, changed = grid.round(use_lines=True)
    assert not changed
    assert grid.count == 26


def part1(inputs: List[str]) -> int:
    grid = LifeGrid(inputs)
    while 1:
        grid, changed = grid.round()
        if not changed:
            return grid.count


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 2424


def part2(inputs) -> int:
    grid = LifeGrid(inputs)
    while 1:
        grid, changed = grid.round(use_lines=True)
        if not changed:
            return grid.count
    return 0


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 2208


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
