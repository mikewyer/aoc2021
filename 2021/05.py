"""Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents
constantly produce large, opaque clouds, so it would be best to avoid them if
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end. These line segments include the points at both
ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2
or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the
following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from 2,2 ->
2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9
-> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in the
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two
lines overlap?
"""

import os
import pytest
import re
from typing import Iterator, List
from collections import namedtuple


@pytest.fixture
def ex_lines() -> List[str]:
    return """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".splitlines()


@pytest.fixture
def ex_render() -> List[str]:
    return """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....""".splitlines()


LineBase = namedtuple("LineBase", ["x1", "y1", "x2", "y2"])


class Line(LineBase):
    @property
    def horizontal(self) -> bool:
        return self.y1 == self.y2

    @property
    def vertical(self) -> bool:
        return self.x1 == self.x2

    @property
    def diagonal(self) -> bool:
        return abs(self.x2 - self.x1) == abs(self.y2 - self.y1)


def parse_lines(lines: List[str]) -> Iterator[Line]:
    for line in lines:
        if matched := re.match(r"(\d+),(\d+) -> (\d+),(\d+)$", line):
            yield Line(
                int(matched[1]), int(matched[2]), int(matched[3]), int(matched[4])
            )


def test_lines(ex_lines: List[str]):
    lines = list(parse_lines(ex_lines))
    assert len(lines) == 10
    perp_lines = [i for i in lines if i.vertical or i.horizontal]
    assert len(perp_lines) == 6


class Grid:
    """Canvas for Lines"""

    def add_line(self, line: Line):
        x = line.x1
        y = line.y1
        while 1:
            # print(f"{x}{y}")
            self.grid[y][x] += 1
            if x == line.x2 and y == line.y2:
                break
            if x < line.x2:
                x += 1
            elif x > line.x2:
                x -= 1
            if y < line.y2:
                y += 1
            elif y > line.y2:
                y -= 1

    def __init__(self, lines: List[Line], diag=False):
        x_max = max([max(i.x1, i.x2) for i in lines])
        y_max = max([max(i.y1, i.y2) for i in lines])
        self.grid: List[List[int]] = [
            [0 for _ in range(0, x_max + 1)] for _ in range(0, y_max + 1)
        ]
        for line in lines:
            # print(line)
            if line.horizontal or line.vertical or diag:
                self.add_line(line)
        # for row in self.grid:
        #     print(row)

    def hot_spots(self):
        count = 0
        for row in self.grid:
            for col in row:
                if col > 1:
                    count += 1
        return count


def test_grid(ex_lines: List[str]):
    grid = Grid(list(parse_lines(ex_lines)))
    assert grid.hot_spots() == 5
    assert Grid(list(parse_lines(ex_lines)), diag=True).hot_spots() == 12


def get_inputs() -> List[str]:
    base, _ = os.path.splitext(os.path.basename(__file__))
    if os.path.exists(base + ".data"):
        return [i.strip() for i in open(base + ".data")]
    return []


def part1(inputs) -> int:
    return Grid(list(parse_lines(inputs))).hot_spots()


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 5167


def part2(inputs) -> int:
    return Grid(list(parse_lines(inputs)), diag=True).hot_spots()


# --- Part Two ---

# Unfortunately, considering only horizontal and vertical lines doesn't give you
# the full picture; you need to also consider diagonal lines.

# Because of the limits of the hydrothermal vent mapping system, the lines in
# your list will only ever be horizontal, vertical, or a diagonal line at exactly
# 45 degrees. In other words:

# An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
# An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
# Considering all lines from the above example would now produce the following diagram:

# 1.1....11.
# .111...2..
# ..2.1.111.
# ...1.2.2..
# .112313211
# ...1.2....
# ..1...1...
# .1.....1..
# 1.......1.
# 222111....
# You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

# Consider all of the lines. At how many points do at least two lines overlap?


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 17604


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
