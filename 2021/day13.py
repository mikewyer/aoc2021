"""Day X"""

import os
import pytest
from typing import List, MutableSet, Tuple


@pytest.fixture
def example() -> List[str]:
    return """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".splitlines()


@pytest.fixture
def example_grid() -> str:
    return """...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........"""


@pytest.fixture
def example_fold() -> str:
    return """#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
..........."""


class Paper:
    def __init__(self, dots_folds: List[str]) -> None:
        self.points: MutableSet[Tuple[int, int]] = set()
        self.folds: List[Tuple[str, int]] = []
        self.max_x = 0
        self.max_y = 0
        for line in dots_folds:
            if line.startswith("fold along"):
                spec = line.split(" ")[2]
                axis, value = spec.split("=")
                self.folds.append((axis, int(value)))
            elif line.strip():
                x, y = [int(i) for i in line.strip().split(",")]
                self.points.add((x, y))
                if x > self.max_x:
                    self.max_x = x
                if y > self.max_y:
                    self.max_y = y
        self.max_x += 1
        self.max_y += 1
        self.next_fold_index = 0

    def point(self, x, y) -> str:
        if (x, y) in self.points:
            return "#"
        return "."

    def __str__(self) -> str:
        return "\n".join(
            [
                "".join([self.point(i, j) for i in range(self.max_x)])
                for j in range(self.max_y)
            ]
        )

    def fold(self, axis: str, val: int):
        x_max = self.max_x
        y_max = self.max_y
        if axis == "x":
            x_max = val
            other = lambda x, y: (self.max_x - x - 1, y)
        else:
            y_max = val
            other = lambda x, y: (x, self.max_y - y - 1)
        for x, y in list(self.points):
            if x > self.max_x or y > self.max_y:
                continue
            if x > x_max or y > y_max:
                # print(f"Adding {other(x,y)} for {x},{y}")
                self.points.add(other(x, y))
        self.max_x = x_max
        self.max_y = y_max

    def next_fold(self):
        axis, value = self.folds[self.next_fold_index]
        self.fold(axis, value)
        self.next_fold_index += 1


def test_example(example: List[str], example_grid: str, example_fold: str):
    paper = Paper(example)
    assert str(paper) == example_grid
    paper.next_fold()
    assert paper.point(0, 0) == "#"
    assert str(paper) == example_fold


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    paper = Paper(inputs)
    paper.next_fold()
    return str(paper).count("#")


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 653


def part2(inputs: List[str]) -> str:  # pylint: disable=unused-argument
    paper = Paper(inputs)
    while paper.next_fold_index < len(paper.folds):
        paper.next_fold()
    return str(paper)


def test_part2() -> None:
    inputs = get_inputs()
    assert (
        part2(inputs)
        == """\
#....#..#.###..####.###..###..###..#..#.
#....#.#..#..#.#....#..#.#..#.#..#.#.#..
#....##...#..#.###..###..#..#.#..#.##...
#....#.#..###..#....#..#.###..###..#.#..
#....#.#..#.#..#....#..#.#....#.#..#.#..
####.#..#.#..#.####.###..#....#..#.#..#."""
    )


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
