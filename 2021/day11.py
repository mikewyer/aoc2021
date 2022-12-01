"""Day X"""

import os
import pytest
from typing import List


@pytest.fixture
def example() -> List[str]:
    return """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()


class OctopusFish:
    def __init__(self, state: int):
        self.state = state
        self.flashed = False
        self.neighbours: List[OctopusFish] = []

    def inc(self):
        self.state += 1

    def check_flash(self) -> int:
        if self.state > 9 and not self.flashed:
            self.flashed = True
            flashes = 1
            for fish in self.neighbours:
                fish.inc()
            for fish in self.neighbours:
                flashes += fish.check_flash()
            return flashes
        return 0

    def reset(self):
        if self.flashed:
            self.state = 0
        self.flashed = False

    def __str__(self):
        return str(self.state)


class Pool:
    def __init__(self, fish_def: List[str]):
        self.rows: List[List[OctopusFish]] = [
            [OctopusFish(int(i)) for i in j] for j in fish_def
        ]
        self.max_row: int = len(self.rows)
        self.max_col: int = len(self.rows[0])
        self.all_fish: List[OctopusFish] = []
        for row in range(self.max_row):
            for col in range(self.max_col):
                fish: OctopusFish = self.rows[row][col]
                self.all_fish.append(fish)
                for i in range(max(0, row - 1), min(self.max_row, row + 2)):
                    for j in range(max(0, col - 1), min(self.max_col, col + 2)):
                        if i == row and j == col:
                            continue
                        fish.neighbours.append(self.rows[i][j])

    def count_flashes(self) -> int:
        total = 0
        for fish in self.all_fish:
            fish.inc()
        for fish in self.all_fish:
            total += fish.check_flash()
        for fish in self.all_fish:
            fish.reset()
        return total

    def __str__(self):
        return "\n".join(["".join([str(j) for j in i]) for i in self.rows])


def test_example(example: List[str]):
    pool = Pool(example)
    assert str(pool.rows[0][0]) == "5"
    assert str(pool) == "\n".join(example)
    print(pool)
    print()
    assert pool.count_flashes() == 0
    print(pool)
    print()
    assert pool.count_flashes() == 35
    print(pool)
    print()
    total = 35
    for _ in range(8):
        total += pool.count_flashes()
    assert total == 204
    for _ in range(90):
        total += pool.count_flashes()
    assert total == 1656


def part1(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    pool = Pool(inputs)
    total = 0
    for _ in range(100):
        total += pool.count_flashes()
    return total


def test_part1() -> None:
    inputs = get_inputs()
    assert part1(inputs) == 1757


def test_all_flash(example: List[str]):
    pool = Pool(example)
    rounds = 1
    while pool.count_flashes() < len(pool.all_fish):
        rounds += 1
    assert rounds == 195


def part2(inputs: List[str]) -> int:  # pylint: disable=unused-argument
    pool = Pool(inputs)
    rounds = 1
    while pool.count_flashes() < len(pool.all_fish):
        rounds += 1
    return rounds


def test_part2() -> None:
    inputs = get_inputs()
    assert part2(inputs) == 422


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
