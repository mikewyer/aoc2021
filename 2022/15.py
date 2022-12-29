"""Day 15"""

from __future__ import annotations
from dataclasses import dataclass
import os
import pytest
import re
from typing import List, Optional, Tuple

INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


@dataclass
class Sensor:
    x: int
    y: int
    b_x: int
    b_y: int
    distance: int = 0

    def __post_init__(self):
        x_diff = abs(self.b_x - self.x)
        y_diff = abs(self.b_y - self.y)
        self.distance = x_diff + y_diff

    @classmethod
    def from_str(cls, input: str):
        nums = [int(i) for i in re.findall(r"-?\d+", input)]
        return Sensor(*nums)

    def row_coverage(self, row: int) -> Optional[Tuple[int, int]]:
        x_width = self.distance - abs(row - self.y)
        if x_width >= 0:
            return self.x - x_width, self.x + x_width
        return None


@pytest.fixture
def example() -> List[str]:
    return [i.strip() for i in INPUT.splitlines()]


def non_beacon_row(
    sensors: List[Sensor],
    row: int,
    bound_x_min: Optional[int] = None,
    bound_x_max: Optional[int] = None,
):
    ranges = []
    for s in sensors:
        if span := s.row_coverage(row):
            min_x, max_x = span
            if bound_x_min is not None and bound_x_max is not None:
                if max_x < bound_x_min:
                    continue
                if min_x > bound_x_max:
                    continue
                min_x = max(min_x, bound_x_min)
                max_x = min(max_x, bound_x_max)
            overlaps = [i for i in ranges if min_x <= i[1] + 1 and max_x >= i[0] - 1]
            others = [i for i in ranges if min_x > i[1] + 1 or max_x < i[0] - 1]
            ranges = others + [
                (
                    min([i[0] for i in overlaps] + [min_x]),
                    max([i[1] for i in overlaps] + [max_x]),
                )
            ]
    return ranges


def count_non_beacon_row(sensors, row):
    ranges = non_beacon_row(sensors, row)
    return sum(i[1] - i[0] for i in ranges)


def find_beacon(sensors, start_num, end_num):
    found = -1
    found_ranges = []
    for row in range(end_num + 1):
        ranges = non_beacon_row(sensors, row, start_num, end_num)
        if len(ranges) > 1:
            print(ranges)
            found = row
            found_ranges = ranges.copy()
            break
    return (found_ranges[0][1] + 1) * 4000000 + found


def test_example(example):
    sensors = [Sensor.from_str(i) for i in example]
    assert len(sensors) == 14
    assert sensors[6].distance == 9
    assert count_non_beacon_row(sensors, 10) == 26
    assert find_beacon(sensors, 0, 20) == 56000011


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    sensors = [Sensor.from_str(i) for i in inputs]
    return count_non_beacon_row(sensors, 2000000)


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 6078701


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    sensors = [Sensor.from_str(i) for i in inputs]
    return find_beacon(sensors, 0, 4000000)


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 12567351400528


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
