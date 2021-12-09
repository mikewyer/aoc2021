"""Day 9"""

import os
import pytest
from typing import Iterable, List, Tuple


@pytest.fixture
def example() -> List[str]:
    return """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


class Grid:
    def __init__(self, inputs: List[str]):
        self.rows = [[int(j) for j in i] for i in inputs]
        self.width = len(self.rows[0])
        self.height = len(self.rows)

    def adjacent(self, x: int, y: int) -> List[Tuple[int, int, int]]:
        cells: List[int] = []
        if y > 0:
            cells.append((self.rows[y - 1][x], x, y - 1))
        if y < self.height - 1:
            cells.append((self.rows[y + 1][x], x, y + 1))
        if x > 0:
            cells.append((self.rows[y][x - 1], x - 1, y))
        if x < self.width - 1:
            cells.append((self.rows[y][x + 1], x + 1, y))
        return cells

    def low_point(self) -> Iterable[Tuple[int, int, int]]:
        for y in range(0, self.height):
            for x in range(0, self.width):
                cell = self.rows[y][x]
                if cell < min([i[0] for i in self.adjacent(x, y)]):
                    yield cell, x, y

    def find_basin(self, start_x: int, start_y: int):
        done = set()
        points = set([(start_x, start_y)])
        count = 0
        todo = list(points)
        while todo and count < 20:
            todo = []
            count += 1
            for x, y in points:
                if (y * self.height + x) not in done:
                    todo.append((x, y))
            for x, y in todo:
                done.add(y * self.height + x)
                for n, new_x, new_y in self.adjacent(x, y):
                    if n < 9 and (new_y * self.height + new_x) not in done:
                        points.add((new_x, new_y))
        return len(points)


def test_example(example: List[str]):
    grid = Grid(example)
    hots = [i[0] for i in grid.low_point()]
    assert hots == [1, 0, 5, 5]
    assert sum([i + 1 for i in hots]) == 15


def test_basin(example: List[str]):
    grid = Grid(example)
    assert grid.find_basin(0, 0) == 3
    assert grid.find_basin(9, 0) == 9
    assert grid.find_basin(2, 2) == 14
    assert grid.find_basin(6, 4) == 9


def part1(inputs) -> int:
    grid = Grid(inputs)
    return sum(i[0] + 1 for i in grid.low_point())


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 489


def part2(inputs) -> int:
    grid = Grid(inputs)
    basins = []
    for _, x, y in grid.low_point():
        basins.append(grid.find_basin(x, y))
    top_3 = sorted(basins)[-3:]
    return top_3[0] * top_3[1] * top_3[2]


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 1056330


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
